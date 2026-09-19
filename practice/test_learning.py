from datetime import date, timedelta
from unittest.mock import patch

from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse

from .courses import COURSES
from .daily_challenges import challenge_for_day
from .gamification import PROGRESS_KEY, REWARDS_KEY, learning_summary, record_activity
from .ielts_courses import BEGINNER_COURSE, LEGACY_IELTS_COURSES
from .ielts_skill_courses import IELTS_COURSES, LESSON_REDIRECTS
from .services import TEST_SESSION_KEY
from . import test_courses


class IeltsCourseTests(TestCase):
    def test_four_skill_courses_each_teach_three_levels(self):
        self.assertEqual(len(IELTS_COURSES), 4)
        self.assertEqual({course.skill for course in IELTS_COURSES}, {"Speaking", "Reading", "Writing", "Listening"})
        for course in IELTS_COURSES:
            with self.subTest(course=course.slug):
                self.assertEqual({lesson.skill for lesson in course.lessons}, {course.skill})
                self.assertEqual({lesson.level for lesson in course.lessons}, {"Beginner", "Intermediate", "Band 8 target"})
                response = self.client.get(reverse("practice:course-detail", args=[course.slug]))
                self.assertContains(response, f"How to approach IELTS {course.skill}")
                for stage in response.context["stages"]:
                    self.assertEqual(len(stage["lessons"]), 2)
                    self.assertContains(response, f'id="{stage["slug"]}"')
                for lesson in course.lessons:
                    page = self.client.get(reverse("practice:course-lesson", args=[course.slug, lesson.slug]))
                    self.assertContains(page, "Your exam technique")
                    self.assertTrue(lesson.technique)
                    if lesson.activity and lesson.activity.kind == "listening":
                        self.assertContains(page, 'id="listening-text"')
                        self.assertContains(page, "Open the transcript")
                    elif lesson.activity and lesson.activity.kind == "speaking":
                        self.assertContains(page, 'id="speaking-timer"')
                        self.assertContains(page, 'name="practised_aloud"')
                    elif lesson.activity:
                        self.assertContains(page, 'class="practice-passage"')
                if course.skill == "Writing":
                    for level in ("beginner", "intermediate", "ielts_8_9"):
                        self.assertContains(response, f"?mode=writing&amp;level={level}")

    def test_listening_map_supplies_the_reference_needed_for_the_route(self):
        page = self.client.get(reverse("practice:course-lesson", args=["ielts-listening", "listening-follow-a-map"]))
        self.assertContains(page, "Campus map")
        self.assertContains(page, "South gate")
        self.assertContains(page, '<th scope="col">West</th>', html=True)
        self.assertContains(page, '<th scope="col">East</th>', html=True)

    def test_speaking_completion_requires_aloud_confirmation(self):
        course = IELTS_COURSES[0]
        lesson = next(item for item in course.lessons if item.skill == "Speaking")
        url = reverse("practice:course-lesson", args=[course.slug, lesson.slug])
        payload = test_courses.CourseTests.response_for(lesson)
        payload.pop("practised_aloud")
        response = self.client.post(url, payload, follow=True)
        self.assertFalse(response.context["lesson_completed"])
        self.assertEqual(response.context["learning"]["xp"], 0)
        response = self.client.post(url, {**payload, "practised_aloud": "on"}, follow=True)
        self.assertTrue(response.context["lesson_completed"])
        self.assertEqual(response.context["learning"]["xp"], 40)

    def test_xp_course_bonus_and_badges_awarded_once(self):
        course = IELTS_COURSES[0]
        for lesson in course.lessons:
            url = reverse("practice:course-lesson", args=[course.slug, lesson.slug])
            self.client.post(url, test_courses.CourseTests.response_for(lesson))
        summary = learning_summary(self.client.session)
        self.assertEqual(summary["xp"], 6 * 40 + 100)
        self.assertEqual(summary["level"], 2)
        earned = {badge["name"] for badge in summary["badges"] if badge["earned"]}
        self.assertEqual(earned, {"First step", "Course finisher"})

        # Repeated success and a later unfinished revision keep, but do not multiply, XP.
        self.client.post(url, test_courses.CourseTests.response_for(lesson))
        self.client.post(url, {"draft": "A revision I will finish later."})
        self.assertEqual(learning_summary(self.client.session)["xp"], summary["xp"])
        self.assertEqual(len(self.client.session[REWARDS_KEY]["active_days"]), 1)

    def test_four_skill_badge_requires_completions_across_the_four_courses(self):
        for index, course in enumerate(IELTS_COURSES):
            lesson = course.lessons[0]
            self.client.post(reverse("practice:course-lesson", args=[course.slug, lesson.slug]), test_courses.CourseTests.response_for(lesson))
            summary = learning_summary(self.client.session)
            badge = next(b for b in summary["badges"] if b["name"] == "Four-skill explorer")
            self.assertEqual(badge["earned"], index == 3)
        self.assertEqual(summary["xp"], 160)

    def test_moved_lessons_restore_saved_work_and_keep_their_local_draft_key(self):
        old_key = (BEGINNER_COURSE.slug, "reading-for-evidence")
        new_key = LESSON_REDIRECTS[old_key]
        lesson = next(item for item in BEGINNER_COURSE.lessons if item.slug == old_key[1])
        attempt = {**test_courses.CourseTests.response_for(lesson), "completed": True, "checked": True}
        original = {old_key[0]: {old_key[1]: attempt}}
        session = self.client.session
        session[PROGRESS_KEY] = original
        session.save()
        old_url = reverse("practice:course-lesson", args=old_key)
        new_url = reverse("practice:course-lesson", args=new_key)
        response = self.client.get(old_url, follow=True)
        self.assertRedirects(response, new_url, status_code=301)
        self.assertEqual(response.context["form"]["draft"].value(), attempt["draft"])
        self.assertTrue(response.context["lesson_completed"])
        self.assertEqual(response.context["learning"]["xp"], 40)
        self.assertContains(response, 'data-draft-key="english-course:ielts-beginner:reading-for-evidence"')
        self.assertEqual(self.client.session[PROGRESS_KEY], original)

        # An old form still open can submit to its original URL, without duplicate XP.
        payload = {**test_courses.CourseTests.response_for(lesson), "draft": attempt["draft"] + " I have reviewed the evidence again."}
        response = self.client.post(old_url, payload, follow=True)
        self.assertRedirects(response, f"{new_url}#lesson-feedback")
        self.assertEqual(response.context["form"]["draft"].value(), payload["draft"])
        self.assertEqual(response.context["learning"]["xp"], 40)
        self.assertNotIn(REWARDS_KEY, self.client.session)
        self.assertEqual(self.client.session[PROGRESS_KEY][new_key[0]][new_key[1]]["draft"], payload["draft"])

    def test_all_old_skill_bookmarks_resolve_and_old_course_overviews_link_to_catalog(self):
        for old_key, new_key in LESSON_REDIRECTS.items():
            with self.subTest(old_key=old_key):
                response = self.client.get(reverse("practice:course-lesson", args=old_key))
                self.assertRedirects(response, reverse("practice:course-lesson", args=new_key), status_code=301)
        for course in LEGACY_IELTS_COURSES:
            response = self.client.get(reverse("practice:course-detail", args=[course.slug]))
            self.assertRedirects(response, f"{reverse('practice:courses')}#ielts-courses", status_code=301)
            # Prior study-plan exercises remain available for their saved work.
            page = self.client.get(reverse("practice:course-lesson", args=[course.slug, course.lessons[0].slug]))
            self.assertEqual(page.status_code, 200)

    def test_old_course_bonus_survives_reorganisation_without_duplicate_lesson_xp(self):
        progress = {BEGINNER_COURSE.slug: {lesson.slug: {"completed": True} for lesson in BEGINNER_COURSE.lessons}}
        summary = learning_summary({PROGRESS_KEY: progress})
        self.assertEqual(summary["completed_lessons"], 6)
        self.assertEqual(summary["completed_courses"], 1)
        self.assertEqual(summary["xp"], 340)
        self.assertEqual(summary["streak"], 0)

    def test_existing_completion_gets_xp_without_inventing_streak_history(self):
        course = COURSES[0]
        session = self.client.session
        session[PROGRESS_KEY] = {course.slug: {course.lessons[0].slug: {"completed": True}}}
        session.save()
        summary = learning_summary(session)
        self.assertEqual(summary["xp"], 40)
        self.assertEqual(summary["streak"], 0)
        self.assertNotIn(REWARDS_KEY, session)


class DailyChallengeTests(TestCase):
    def setUp(self):
        self.today = date(2026, 9, 19)
        clock_patch = patch("practice.views.learning_day", return_value=self.today)
        self.clock = clock_patch.start()
        self.addCleanup(clock_patch.stop)
        self.url = reverse("practice:daily-challenge")
        self.home = reverse("practice:landing")
        self.challenge = challenge_for_day(self.today)

    def payload(self, day=None, answer=None):
        day = day or self.today
        return {"date": day.isoformat(), "answer": str(challenge_for_day(day).question.correct if answer is None else answer)}

    def test_daily_cta_is_deterministic_and_visiting_does_not_earn_xp(self):
        first = self.client.get(self.home)
        other = Client().get(self.home)
        self.assertEqual(first.context["daily"], other.context["daily"])
        self.assertContains(first, 'id="daily-challenge"')
        self.assertContains(first, self.url)
        self.assertContains(first, self.challenge.word)
        self.assertEqual(first.context["learning"]["xp"], 0)
        self.assertNotIn(REWARDS_KEY, self.client.session)
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_wrong_answer_can_be_retried_and_success_only_earns_once(self):
        wrong = (self.challenge.question.correct + 1) % len(self.challenge.question.options)
        response = self.client.post(self.url, self.payload(answer=wrong), follow=True)
        self.assertFalse(response.context["daily_solved"])
        self.assertTrue(response.context["daily_checked"])
        self.assertEqual(response.context["learning"]["xp"], 0)
        self.assertEqual(response.context["daily_selected"], wrong)
        self.assertContains(response, "Keep going")

        response = self.client.post(self.url, self.payload(), follow=True)
        self.assertRedirects(response, f"{self.home}#daily-challenge")
        self.assertTrue(response.context["daily_solved"])
        self.assertEqual(response.context["learning"]["xp"], 15)
        self.assertEqual(response.context["learning"]["streak"], 1)
        saved = dict(self.client.session)
        for answer in (self.challenge.question.correct, wrong):
            response = self.client.post(self.url, self.payload(answer=answer), follow=True)
            self.assertTrue(response.context["daily_solved"])
            self.assertEqual(response.context["learning"]["xp"], 15)
            self.assertEqual(dict(self.client.session), saved)

    def test_stale_future_and_invalid_answers_do_not_change_rewards(self):
        self.client.post(self.url, self.payload())
        saved = dict(self.client.session)
        for payload in (
            {}, {"date": self.today.isoformat()}, self.payload(answer="999"),
            self.payload(answer="not-an-option"),
            self.payload(day=self.today - timedelta(days=1)),
            self.payload(day=self.today + timedelta(days=1)),
        ):
            with self.subTest(payload=payload):
                response = self.client.post(self.url, payload)
                self.assertEqual(response.status_code, 400)
                self.assertTrue(response.context["daily_error"])
                self.assertEqual(response.context["daily"], self.challenge)
                self.assertEqual(dict(self.client.session), saved)

    def test_day_rollover_serves_new_question_and_rejects_open_old_form(self):
        self.client.post(self.url, self.payload())
        tomorrow = self.today + timedelta(days=1)
        self.clock.return_value = tomorrow
        response = self.client.get(self.home)
        self.assertNotEqual(response.context["daily"], self.challenge)
        self.assertFalse(response.context["daily_solved"])
        self.assertFalse(response.context["daily_checked"])
        self.assertEqual(response.context["learning"]["streak"], 1)
        response = self.client.post(self.url, self.payload())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.context["daily_date"], tomorrow)
        response = self.client.post(self.url, self.payload(day=tomorrow), follow=True)
        self.assertEqual(response.context["learning"]["xp"], 30)
        self.assertEqual(response.context["learning"]["streak"], 2)

    def test_rewards_restore_with_session_and_are_isolated_from_tests_and_others(self):
        session = self.client.session
        session[TEST_SESSION_KEY] = "existing-test"
        session.save()
        self.client.post(self.url, self.payload())
        restored = Client()
        restored.cookies = self.client.cookies.copy()
        page = restored.get(self.home)
        self.assertTrue(page.context["daily_solved"])
        self.assertEqual(page.context["learning"]["xp"], 15)
        self.assertEqual(restored.session[TEST_SESSION_KEY], "existing-test")
        self.assertFalse(Client().get(self.home).context["daily_solved"])

    def test_daily_submission_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.get(self.home)
        self.assertEqual(client.post(self.url, self.payload()).status_code, 403)
        payload = {**self.payload(), "csrfmiddlewaretoken": client.cookies["csrftoken"].value}
        self.assertEqual(client.post(self.url, payload).status_code, 302)


class StreakTests(SimpleTestCase):
    def test_same_day_activity_deduplicates_and_gap_resets_current_streak(self):
        session = {}
        start = date(2026, 9, 1)
        for offset in range(7):
            day = start + timedelta(days=offset)
            record_activity(session, today=day, daily=True)
            record_activity(session, today=day, daily=True)
            record_activity(session, today=day)
        summary = learning_summary(session, today=start + timedelta(days=6))
        self.assertEqual(summary["streak"], 7)
        self.assertEqual(summary["xp"], 105)
        self.assertEqual(summary["best_streak"], 7)
        self.assertTrue(next(b for b in summary["badges"] if b["name"] == "Week in motion")["earned"])
        self.assertEqual(learning_summary(session, today=start + timedelta(days=7))["streak"], 7)
        self.assertEqual(learning_summary(session, today=start + timedelta(days=8))["streak"], 0)
        record_activity(session, today=start + timedelta(days=9))
        summary = learning_summary(session, today=start + timedelta(days=9))
        self.assertEqual(summary["streak"], 1)
        self.assertEqual(summary["best_streak"], 7)
        self.assertTrue(summary["week"][-1]["active"])
        self.assertFalse(summary["week"][-2]["active"])

    def test_unknown_saved_lessons_do_not_create_xp_or_badges(self):
        session = {PROGRESS_KEY: {"missing": {"made-up": {"completed": True}}}}
        self.assertEqual(learning_summary(session)["xp"], 0)
