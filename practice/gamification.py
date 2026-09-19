"""Session-scoped rewards. Course XP is derived from saved completions, never POST counts."""

from datetime import date, timedelta

from django.utils import timezone

from .courses import ARCHIVED_COURSES, COURSES
from .course_progress import resolved_progress
from .ielts_skill_courses import LESSON_REDIRECTS


PROGRESS_KEY = "course_progress"
REWARDS_KEY = "learning_rewards"
LESSON_XP = 40
COURSE_XP = 100
DAILY_XP = 15
LEVEL_XP = 200


def learning_day() -> date:
    """A single UTC boundary for both challenges and streaks, including POST validation."""
    return timezone.now().date()


def record_activity(session, *, daily=False, today=None):
    today = today or learning_day()
    rewards = session.get(REWARDS_KEY, {})
    active_days = set(rewards.get("active_days", []))
    active_days.add(today.isoformat())
    solved = set(rewards.get("daily_solved", []))
    if daily:
        solved.add(today.isoformat())
    session[REWARDS_KEY] = {
        "active_days": sorted(active_days),
        "daily_solved": sorted(solved),
    }


def learning_summary(session, *, today=None):
    today = today or learning_day()
    progress = resolved_progress(session.get(PROGRESS_KEY, {}))
    rewards = session.get(REWARDS_KEY, {})
    completed_lessons = set()
    completed_courses = 0
    ielts_skills = set()
    for course in (*COURSES, *ARCHIVED_COURSES):
        saved = progress.get(course.slug, {})
        finished = [lesson for lesson in course.lessons if saved.get(lesson.slug, {}).get("completed")]
        completed_lessons.update(LESSON_REDIRECTS.get((course.slug, lesson.slug), (course.slug, lesson.slug)) for lesson in finished)
        completed_courses += len(finished) == len(course.lessons)
        if course.is_ielts:
            ielts_skills.update(lesson.skill for lesson in finished)

    active_days = {date.fromisoformat(day) for day in rewards.get("active_days", [])}
    active_days = {day for day in active_days if day <= today}
    daily_count = len({day for day in rewards.get("daily_solved", []) if day <= today.isoformat()})
    streak = 0
    cursor = today if today in active_days else today - timedelta(days=1)
    while cursor in active_days:
        streak += 1
        cursor -= timedelta(days=1)
    best_streak = run = 0
    previous = None
    for day in sorted(active_days):
        run = run + 1 if previous and day == previous + timedelta(days=1) else 1
        best_streak = max(best_streak, run)
        previous = day

    completed_count = len(completed_lessons)
    xp = completed_count * LESSON_XP + completed_courses * COURSE_XP + daily_count * DAILY_XP
    badge_definitions = (
        ("First step", "Complete your first lesson or daily challenge.", completed_count + daily_count >= 1),
        ("Week in motion", "Practise on seven consecutive UTC days.", best_streak >= 7),
        ("Course finisher", "Complete every lesson in any course.", completed_courses >= 1),
        ("Four-skill explorer", "Complete an IELTS lesson in listening, reading, speaking, and writing.", {"Listening", "Reading", "Speaking", "Writing"} <= ielts_skills),
    )
    return {
        "xp": xp,
        "level": xp // LEVEL_XP + 1,
        "level_progress": xp % LEVEL_XP,
        "level_max": LEVEL_XP,
        "xp_to_next_level": LEVEL_XP - xp % LEVEL_XP,
        "streak": streak,
        "best_streak": best_streak,
        "active_today": today in active_days,
        "completed_lessons": completed_count,
        "completed_courses": completed_courses,
        "daily_count": daily_count,
        "badges": [{"name": name, "description": description, "earned": earned} for name, description, earned in badge_definitions],
        "week": [
            {"date": day, "active": day in active_days, "today": day == today}
            for offset in range(6, -1, -1)
            for day in [today - timedelta(days=offset)]
        ],
    }
