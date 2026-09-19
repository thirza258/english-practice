from __future__ import annotations

from django import forms
from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods

from .courses import COURSES, Course, Lesson
from .gamification import PROGRESS_KEY, learning_summary, record_activity
from .nlp import WORD_RE
from .views import CANONICAL_HOST


MAX_DRAFT_LENGTH = 10000


def _course(slug: str) -> Course:
    for course in COURSES:
        if course.slug == slug:
            return course
    raise Http404("Course not found.")


def _course_summary(course: Course, progress: dict) -> dict:
    saved = progress.get(course.slug, {})
    lessons = [
        {
            "lesson": lesson,
            "number": index + 1,
            "completed": bool(saved.get(lesson.slug, {}).get("completed")),
        }
        for index, lesson in enumerate(course.lessons)
    ]
    completed = sum(item["completed"] for item in lessons)
    next_lesson = next(
        (item["lesson"] for item in lessons if not item["completed"]),
        course.lessons[0],
    )
    return {
        "course": course,
        "lessons": lessons,
        "completed_count": completed,
        "percent": round(completed / len(lessons) * 100),
        "is_complete": completed == len(lessons),
        "next_lesson": next_lesson,
    }


class LessonForm(forms.Form):
    def __init__(self, lesson: Lesson, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for index, question in enumerate(lesson.questions):
            self.fields[f"question_{index}"] = forms.ChoiceField(
                label=question.prompt,
                choices=[(str(i), option) for i, option in enumerate(question.options)],
                required=False,
                widget=forms.RadioSelect,
            )
        self.fields["draft"] = forms.CharField(
            label=lesson.assignment.label,
            required=False,
            max_length=MAX_DRAFT_LENGTH,
            widget=forms.Textarea(attrs={
                "rows": 10,
                "placeholder": "Write your response here…",
                "aria-describedby": "assignment-prompt draft-help draft-count draft-status",
            }),
        )
        self.fields["reviewed"] = forms.BooleanField(
            label="I have checked my work against the checklist.",
            required=False,
        )
        if lesson.activity and lesson.activity.kind == "speaking":
            self.fields["practised_aloud"] = forms.BooleanField(
                label="I practised the speaking prompt aloud.", required=False,
            )


@require_GET
def course_list(request: HttpRequest):
    progress = request.session.get(PROGRESS_KEY, {})
    return render(request, "practice/courses.html", {
        "courses": [_course_summary(course, progress) for course in COURSES],
        "course_count": len(COURSES),
        "lesson_count": sum(len(course.lessons) for course in COURSES),
        "learning": learning_summary(request.session),
        "canonical_url": f"{CANONICAL_HOST}{reverse('practice:courses')}",
    })


@require_GET
def course_detail(request: HttpRequest, course_slug: str):
    course = _course(course_slug)
    return render(request, "practice/course_detail.html", {
        **_course_summary(course, request.session.get(PROGRESS_KEY, {})),
        "learning": learning_summary(request.session),
        "canonical_url": f"{CANONICAL_HOST}{request.path}",
    })


@require_http_methods(["GET", "POST"])
def course_lesson(request: HttpRequest, course_slug: str, lesson_slug: str):
    course = _course(course_slug)
    lesson_index = next(
        (i for i, lesson in enumerate(course.lessons) if lesson.slug == lesson_slug),
        None,
    )
    if lesson_index is None:
        raise Http404("Lesson not found in this course.")
    lesson = course.lessons[lesson_index]
    progress = request.session.get(PROGRESS_KEY, {})
    attempt = progress.get(course.slug, {}).get(lesson.slug, {})
    form = LessonForm(lesson, request.POST if request.method == "POST" else None, initial=attempt)

    if request.method == "POST" and form.is_valid():
        attempt_complete = (
            all(form.cleaned_data[f"question_{i}"] == str(question.correct)
                for i, question in enumerate(lesson.questions))
            and len(WORD_RE.findall(form.cleaned_data["draft"])) >= lesson.assignment.min_words
            and form.cleaned_data["reviewed"]
            and ("practised_aloud" not in form.fields or form.cleaned_data["practised_aloud"])
        )
        if attempt_complete and not attempt.get("completed"):
            record_activity(request.session)
        attempt = {
            **form.cleaned_data,
            "checked": True,
            "completed": bool(attempt.get("completed") or attempt_complete),
        }
        progress.setdefault(course.slug, {})[lesson.slug] = attempt
        request.session[PROGRESS_KEY] = progress
        return redirect(f"{request.path}#lesson-feedback")

    checked = bool(attempt.get("checked")) and not form.is_bound
    questions = []
    correct_count = 0
    for index, question in enumerate(lesson.questions):
        field = form[f"question_{index}"]
        correct = field.value() == str(question.correct)
        correct_count += correct
        questions.append({
            "field": field,
            "correct": correct,
            "explanation": question.explanation,
            "answer": question.options[question.correct],
        })
    word_count = len(WORD_RE.findall(form["draft"].value() or ""))
    return render(request, "practice/course_lesson.html", {
        **_course_summary(course, progress),
        "lesson": lesson,
        "lesson_number": lesson_index + 1,
        "previous_lesson": course.lessons[lesson_index - 1] if lesson_index else None,
        "next_in_order": course.lessons[lesson_index + 1] if lesson_index + 1 < len(course.lessons) else None,
        "form": form,
        "questions": questions,
        "checked": checked,
        "correct_count": correct_count,
        "word_count": word_count,
        "writing_long_enough": word_count >= lesson.assignment.min_words,
        "lesson_completed": bool(attempt.get("completed")),
        "learning": learning_summary(request.session),
        "canonical_url": f"{CANONICAL_HOST}{request.path}",
    }, status=400 if form.is_bound else 200)
