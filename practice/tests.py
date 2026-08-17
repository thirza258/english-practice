from __future__ import annotations

from django.test import TestCase
from django.urls import reverse


class PracticePageTests(TestCase):
    def test_landing_page_has_seo_and_test_link(self) -> None:
        response = self.client.get(reverse("practice:landing"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "English Practice Diagnostic")
        self.assertContains(response, 'meta name="description"', html=False)
        self.assertContains(response, 'content="index,follow"', html=False)
        self.assertContains(response, reverse("practice:test"))

    def test_test_page_is_noindex_and_has_quiz_controls(self) -> None:
        response = self.client.get(reverse("practice:test"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'content="noindex,nofollow"', html=False)
        self.assertContains(response, "Submit Answer")
        self.assertContains(response, reverse("practice:landing"))
