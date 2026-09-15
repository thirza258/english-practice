from __future__ import annotations

from django.test import Client, TestCase
from django.urls import reverse
from django.utils.html import escape

from .courses import COURSES
from .course_views import MAX_DRAFT_LENGTH, PROGRESS_KEY
from .services import TEST_SESSION_KEY


class CourseTests(TestCase):
    def setUp(self):
        self.course = COURSES[0]
        self.lesson = self.course.lessons[0]
        self.url = reverse("practice:course-lesson", args=[self.course.slug, self.lesson.slug])

    @staticmethod
    def response_for(lesson):
        return {
            **{f"question_{i}": str(question.correct) for i, question in enumerate(lesson.questions)},
            "draft": lesson.assignment.sample,
            "reviewed": "on",
        }

    def test_courses_are_discoverable_and_every_lesson_renders(self):
        home = self.client.get(reverse("practice:landing"))
        catalog = self.client.get(reverse("practice:courses"))
        sitemap = self.client.get(reverse("practice:sitemap-xml"))
        self.assertContains(home, reverse("practice:courses"))
        for course in COURSES:
            detail_url = reverse("practice:course-detail", args=[course.slug])
            detail = self.client.get(detail_url)
            self.assertContains(home, detail_url)
            self.assertContains(catalog, detail_url)
            self.assertContains(sitemap, f"https://english.nevatal.id{detail_url}")
            for lesson in course.lessons:
                url = reverse("practice:course-lesson", args=[course.slug, lesson.slug])
                with self.subTest(url=url):
                    self.assertContains(detail, url)
                    self.assertContains(sitemap, f"https://english.nevatal.id{url}")
                    page = self.client.get(url)
                    self.assertContains(page, escape(lesson.title))
                    self.assertContains(page, 'name="draft"')
                    self.assertFalse(page.context["checked"])
                    self.assertNotContains(page, 'class="question-explanation')
        self.assertNotIn(PROGRESS_KEY, self.client.session)

    def test_unknown_course_or_lesson_returns_404(self):
        urls = [
            reverse("practice:course-detail", args=["missing"]),
            reverse("practice:course-lesson", args=["missing", self.lesson.slug]),
            reverse("practice:course-lesson", args=[self.course.slug, "missing"]),
            reverse("practice:course-lesson", args=[self.course.slug, COURSES[1].lessons[0].slug]),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)

    def test_success_saves_work_and_resumes_at_next_unfinished_lesson(self):
        payload = self.response_for(self.lesson)
        response = self.client.post(self.url, payload, follow=True)
        self.assertRedirects(response, f"{self.url}#lesson-feedback")
        self.assertContains(response, "Lesson complete")
        self.assertEqual(response.context["completed_count"], 1)
        self.assertEqual(response.context["percent"], 25)

        # A fresh client with the same cookies restores the database session.
        restored_client = Client()
        restored_client.cookies = self.client.cookies.copy()
        restored = restored_client.get(self.url)
        self.assertEqual(restored.context["form"]["draft"].value(), payload["draft"])
        self.assertEqual(restored.context["form"]["question_0"].value(), payload["question_0"])
        detail = restored_client.get(reverse("practice:course-detail", args=[self.course.slug]))
        self.assertEqual(detail.context["next_lesson"], self.course.lessons[1])

    def test_each_completion_requirement_is_enforced_and_drafts_are_saved(self):
        cases = (
            {"question_0": str((self.lesson.questions[0].correct + 1) % 3)},
            {"question_0": ""},
            {"draft": "A short draft."},
            {"draft": " ", "reviewed": ""},
            {"reviewed": ""},
        )
        for change in cases:
            with self.subTest(change=change):
                client = Client()
                payload = {**self.response_for(self.lesson), **change}
                response = client.post(self.url, payload, follow=True)
                self.assertEqual(response.status_code, 200)
                self.assertFalse(response.context["lesson_completed"])
                self.assertEqual(response.context["completed_count"], 0)
                saved = client.session[PROGRESS_KEY][self.course.slug][self.lesson.slug]
                self.assertEqual(saved["draft"], payload["draft"].strip())
                self.assertContains(response, "Your practice check")
                self.assertContains(response, escape(self.lesson.questions[0].explanation))

    def test_invalid_answers_and_oversized_drafts_do_not_overwrite_saved_work(self):
        self.client.post(self.url, self.response_for(self.lesson))
        original = self.client.session[PROGRESS_KEY]
        for change in ({"question_0": "999"}, {"draft": "x" * (MAX_DRAFT_LENGTH + 1)}):
            with self.subTest(change=list(change)):
                response = self.client.post(self.url, {**self.response_for(self.lesson), **change})
                self.assertEqual(response.status_code, 400)
                self.assertTrue(response.context["form"].errors)
                self.assertEqual(self.client.session[PROGRESS_KEY], original)

    def test_retry_keeps_completed_progress_and_updates_latest_draft(self):
        self.client.post(self.url, self.response_for(self.lesson))
        revised = "A different draft that I will develop later."
        response = self.client.post(self.url, {"draft": revised}, follow=True)
        self.assertEqual(response.context["correct_count"], 0)
        self.assertTrue(response.context["lesson_completed"])
        self.assertEqual(response.context["form"]["draft"].value(), revised)
        self.assertEqual(response.context["completed_count"], 1)

    def test_course_completion_across_all_three_courses(self):
        for course in COURSES:
            for lesson in course.lessons:
                url = reverse("practice:course-lesson", args=[course.slug, lesson.slug])
                response = self.client.post(url, self.response_for(lesson), follow=True)
                self.assertTrue(response.context["lesson_completed"], lesson.slug)
            detail = self.client.get(reverse("practice:course-detail", args=[course.slug]))
            self.assertTrue(detail.context["is_complete"])
            self.assertEqual(detail.context["percent"], 100)
            self.assertContains(detail, "Course complete!")
        catalog = self.client.get(reverse("practice:courses"))
        self.assertTrue(all(item["is_complete"] for item in catalog.context["courses"]))

    def test_progress_is_isolated_from_other_learners_and_diagnostic_tests(self):
        session = self.client.session
        session[TEST_SESSION_KEY] = "existing-diagnostic-session"
        session.save()
        self.client.post(self.url, self.response_for(self.lesson))
        self.assertEqual(self.client.session[TEST_SESSION_KEY], "existing-diagnostic-session")
        other_client = Client()
        page = other_client.get(self.url)
        self.assertEqual(page.context["completed_count"], 0)
        self.assertFalse(page.context["form"]["draft"].value())
        other_course = self.client.get(reverse("practice:course-detail", args=[COURSES[1].slug]))
        self.assertEqual(other_course.context["completed_count"], 0)

    def test_submission_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.get(self.url)
        response = client.post(self.url, self.response_for(self.lesson))
        self.assertEqual(response.status_code, 403)
        payload = {**self.response_for(self.lesson), "csrfmiddlewaretoken": client.cookies["csrftoken"].value}
        self.assertEqual(client.post(self.url, payload).status_code, 302)

    def test_saved_writing_is_escaped_in_html(self):
        payload = self.response_for(self.lesson)
        payload["draft"] += ' <script>alert("hello")</script>'
        page = self.client.post(self.url, payload, follow=True)
        self.assertNotContains(page, '<script>alert("hello")</script>')
        self.assertContains(page, "&lt;script&gt;")
