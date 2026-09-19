"""Resolve moved lessons without losing drafts or counting a lesson twice."""

from .ielts_skill_courses import LESSON_REDIRECTS


def resolved_progress(progress):
    result = {slug: dict(lessons) for slug, lessons in progress.items()}
    for (old_course, old_lesson), (new_course, new_lesson) in LESSON_REDIRECTS.items():
        old = progress.get(old_course, {}).get(old_lesson, {})
        new = progress.get(new_course, {}).get(new_lesson, {})
        if old or new:
            # New submissions own the latest draft; completion remains cumulative.
            attempt = {**old, **new, "completed": bool(old.get("completed") or new.get("completed"))}
            result.setdefault(new_course, {})[new_lesson] = attempt
            result.setdefault(old_course, {})[old_lesson] = attempt
    return result
