from __future__ import annotations

import json
from django.test import TestCase
from django.urls import reverse

from .ai import _validate_paragraph, _validate_question
from .models import ParagraphBankQuestion, QuestionBankQuestion, TestSession
from .question_bank import PARAGRAPH_BANK, QUESTION_BANK, ParagraphBlueprint, QuestionBlueprint
from .services import (
    build_results,
    create_paragraph_test_state,
    create_test_state,
    current_question_payload,
    normalize_level,
    normalize_mode,
    public_paragraph_payload,
    public_question_payload,
    submit_answer,
)


class PracticePageTests(TestCase):
    def test_landing_page_has_seo_and_level_links(self) -> None:
        response = self.client.get(reverse("practice:landing"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Grammar and paragraph practice.")
        self.assertContains(response, "Sentence practice")
        self.assertContains(response, "Beginner")
        self.assertContains(response, "Intermediate")
        self.assertContains(response, "Advanced")
        self.assertContains(response, "IELTS 8.0–9.0")
        self.assertContains(response, "All levels")
        self.assertContains(response, f'{reverse("practice:test")}?mode=paragraph&level=beginner')
        self.assertContains(response, f'{reverse("practice:test")}?mode=sentence&level=beginner')
        self.assertContains(response, f'{reverse("practice:test")}?mode=paragraph&level=ielts_8_9')
        self.assertContains(response, f'{reverse("practice:test")}?mode=sentence&level=ielts_8_9')
        self.assertContains(response, 'href="https://english.nevatal.id/"')
        self.assertContains(response, 'content="https://english.nevatal.id/"')

    def test_test_page_is_noindex_and_has_quiz_controls_and_level_pill(self) -> None:
        response = self.client.get(reverse("practice:test"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'content="noindex,nofollow"', html=False)
        self.assertContains(response, "Submit Answer")
        self.assertContains(response, "modePill")
        self.assertContains(response, "levelPill")
        self.assertContains(response, 'data-action="retry-mode"')
        self.assertContains(response, 'data-action="retry-level"')
        self.assertContains(response, 'data-level="ielts_8_9"')
        self.assertContains(response, reverse("practice:landing"))
        self.assertContains(response, 'href="https://english.nevatal.id/test/"')

    def test_test_page_with_mode_and_level_query_params(self) -> None:
        response = self.client.get(reverse("practice:test") + "?mode=paragraph&level=ielts_8_9")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'requestedLevel: "ielts_8_9"')
        self.assertContains(response, 'requestedMode: "paragraph"')

    def test_robots_txt_seo_and_sitemap(self) -> None:
        response = self.client.get(reverse("practice:robots-txt"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/plain", response["Content-Type"])
        self.assertContains(response, "User-agent: *")
        self.assertContains(response, "Allow: /")
        self.assertContains(response, "Disallow: /api/")
        self.assertContains(response, "Sitemap: https://english.nevatal.id/sitemap.xml")

    def test_sitemap_xml_seo(self) -> None:
        response = self.client.get(reverse("practice:sitemap-xml"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("application/xml", response["Content-Type"])
        self.assertContains(response, "https://english.nevatal.id/")
        self.assertContains(response, "https://english.nevatal.id/test/")
        self.assertContains(response, "<urlset")


class LevelAndModeServiceTests(TestCase):
    def setUp(self) -> None:
        QuestionBankQuestion.seed_from_static_bank()
        ParagraphBankQuestion.seed_from_static_bank()

    def test_normalize_level_and_mode(self) -> None:
        self.assertEqual(normalize_level("beginner"), "beginner")
        self.assertEqual(normalize_level("Beginner"), "beginner")
        self.assertEqual(normalize_level("INTERMEDIATE"), "intermediate")
        self.assertEqual(normalize_level("advanced"), "advanced")
        self.assertEqual(normalize_level("ielts_8_9"), "ielts_8_9")
        self.assertEqual(normalize_level("ielts"), "ielts_8_9")
        self.assertEqual(normalize_level("ielts 8-9"), "ielts_8_9")
        self.assertEqual(normalize_level("all"), "all")
        self.assertEqual(normalize_level("unknown_level"), "all")
        self.assertEqual(normalize_level(None), "all")

        self.assertEqual(normalize_mode("sentence"), "sentence")
        self.assertEqual(normalize_mode("paragraph"), "paragraph")
        self.assertEqual(normalize_mode("PARAGRAPH"), "paragraph")
        self.assertEqual(normalize_mode("unknown_mode"), "sentence")
        self.assertEqual(normalize_mode(None), "sentence")

    def test_create_sentence_test_states(self) -> None:
        for lvl in ["beginner", "intermediate", "advanced", "ielts_8_9", "all"]:
            state = create_test_state(total_questions=10, level=lvl)
            self.assertEqual(state["level"], lvl)
            self.assertEqual(state["mode"], "sentence")
            self.assertEqual(len(state["questions"]), 10)
            for q in state["questions"]:
                if lvl != "all":
                    self.assertEqual(q["level"], lvl)
                self.assertEqual(len(q["options"]), 5)
                self.assertIn(q["correct_answer"], ["A", "B", "C", "D", "E"])

    def test_create_paragraph_test_states(self) -> None:
        for lvl in ["beginner", "intermediate", "advanced", "ielts_8_9", "all"]:
            state = create_paragraph_test_state(total_paragraphs=3, level=lvl)
            self.assertEqual(state["level"], lvl)
            self.assertEqual(state["mode"], "paragraph")
            self.assertEqual(state["test_type"], "paragraph")
            self.assertGreaterEqual(state["total_paragraphs"], 1)
            self.assertGreaterEqual(state["total_questions"], 3)

            for p in state["questions"]:
                if lvl != "all":
                    self.assertEqual(p["level"], lvl)
                self.assertIn("title", p)
                self.assertIn("text_with_blanks", p)
                self.assertIn("full_text", p)
                self.assertIn("paragraph_explanation", p)
                self.assertGreaterEqual(len(p["blanks"]), 2)
                for b in p["blanks"]:
                    self.assertEqual(len(b["options"]), 5)
                    self.assertIn(b["correct_answer"], ["A", "B", "C", "D", "E"])

    def test_ielts_sentence_rare_words_present(self) -> None:
        state = create_test_state(total_questions=10, level="ielts_8_9")
        self.assertEqual(state["level"], "ielts_8_9")
        found_rare_word = False
        rare_markers = ["cogent", "obfuscate", "salutary", "perspicacious", "dichotomy", "lacuna", "exacerbate", "notwithstanding", "antithetical", "conspicuous", "scarcely", "seldom"]
        for q in state["questions"]:
            text_combo = (q["question"] + " " + q["correct_answer_text"] + " " + q["explanation"]).lower()
            if any(marker in text_combo for marker in rare_markers):
                found_rare_word = True
                break
        self.assertTrue(found_rare_word, "Expected IELTS 8-9 questions to feature rare/advanced academic vocabulary.")

    def test_sentence_hidden_topic_principle(self) -> None:
        state = create_test_state(total_questions=10, level="beginner")
        current_q = current_question_payload(state)
        self.assertIsNotNone(current_q)
        self.assertNotIn("grammar_topic", current_q)
        self.assertNotIn("topic", current_q)
        self.assertNotIn("rule", current_q)
        self.assertNotIn("correct_answer", current_q)

        correct_choice = state["questions"][0]["correct_answer"]
        wrong_choice = "B" if correct_choice == "A" else "A"

        # Test correct answer
        result_corr = submit_answer(state, correct_choice)
        self.assertIn("feedback", result_corr)
        fb_corr = result_corr["feedback"]
        self.assertTrue(fb_corr["is_correct"])
        self.assertIn("grammar_topic", fb_corr)
        self.assertIn("level", fb_corr)
        self.assertIn("rule", fb_corr)
        self.assertIn("explanation", fb_corr)
        self.assertEqual(fb_corr["reason_right"], state["questions"][0]["explanation"])
        self.assertEqual(fb_corr["reason_wrong"], "-")

        # Test incorrect answer on question 2
        result_wrong = submit_answer(state, wrong_choice)
        fb_wrong = result_wrong["feedback"]
        self.assertFalse(fb_wrong["is_correct"])
        self.assertEqual(fb_wrong["reason_right"], "-")
        self.assertNotEqual(fb_wrong["reason_wrong"], "-")
        self.assertIn("does not fit because", fb_wrong["reason_wrong"])

        # Test results payload
        results = build_results(state)
        self.assertEqual(results["questions"][0]["reason_right"], state["questions"][0]["explanation"])
        self.assertEqual(results["questions"][0]["reason_wrong"], "-")
        self.assertEqual(results["questions"][1]["reason_right"], "-")
        self.assertNotEqual(results["questions"][1]["reason_wrong"], "-")

    def test_paragraph_hidden_topic_and_submission(self) -> None:
        state = create_paragraph_test_state(total_paragraphs=2, level="ielts_8_9")
        current_p = current_question_payload(state)
        self.assertIsNotNone(current_p)
        self.assertIn("title", current_p)
        self.assertIn("text_with_blanks", current_p)
        self.assertIn("blanks", current_p)

        # Before submission, blanks do not reveal correct answer or rules
        for b in current_p["blanks"]:
            self.assertNotIn("correct_answer", b)
            self.assertNotIn("grammar_topic", b)
            self.assertNotIn("rule", b)
            self.assertNotIn("explanation", b)

        # Build answers: 1st blank correct, 2nd blank wrong
        p_blanks = state["questions"][0]["blanks"]
        corr_1 = p_blanks[0]["correct_answer"]
        corr_2 = p_blanks[1]["correct_answer"]
        wrong_2 = "B" if corr_2 == "A" else "A"

        answers = {
            str(p_blanks[0]["blank_id"]): corr_1,
            str(p_blanks[1]["blank_id"]): wrong_2,
        }
        for b in p_blanks[2:]:
            answers[str(b["blank_id"])] = b["correct_answer"]

        result = submit_answer(state, answers)
        self.assertIn("feedback", result)
        fb = result["feedback"]
        self.assertFalse(fb["all_correct"])
        self.assertIn("paragraph_explanation", fb)
        self.assertIn("full_text", fb)
        self.assertEqual(len(fb["blanks_feedback"]), len(p_blanks))

        # Blank 1 was correct: reason_right is explanation, reason_wrong is "-"
        b1_fb = fb["blanks_feedback"][0]
        self.assertTrue(b1_fb["is_correct"])
        self.assertEqual(b1_fb["reason_right"], p_blanks[0]["explanation"])
        self.assertEqual(b1_fb["reason_wrong"], "-")

        # Blank 2 was wrong: reason_right is "-", reason_wrong explains why wrong
        b2_fb = fb["blanks_feedback"][1]
        self.assertFalse(b2_fb["is_correct"])
        self.assertEqual(b2_fb["reason_right"], "-")
        self.assertNotEqual(b2_fb["reason_wrong"], "-")
        self.assertIn("does not fit because", b2_fb["reason_wrong"])

        # Check results payload
        results = build_results(state)
        p0_blanks = results["paragraphs"][0]["blanks"]
        self.assertEqual(p0_blanks[0]["reason_right"], p_blanks[0]["explanation"])
        self.assertEqual(p0_blanks[0]["reason_wrong"], "-")
        self.assertEqual(p0_blanks[1]["reason_right"], "-")
        self.assertNotEqual(p0_blanks[1]["reason_wrong"], "-")


class APITests(TestCase):
    def setUp(self) -> None:
        QuestionBankQuestion.seed_from_static_bank()
        ParagraphBankQuestion.seed_from_static_bank()

    def test_start_sentence_test_api_ielts(self) -> None:
        response = self.client.post(
            reverse("practice:test-start"),
            data=json.dumps({"level": "ielts_8_9", "mode": "sentence"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["level"], "ielts_8_9")
        self.assertEqual(data["mode"], "sentence")
        self.assertIn("test_id", data)
        self.assertIn("question", data)
        self.assertEqual(data["total_questions"], 10)

    def test_start_paragraph_test_api_ielts(self) -> None:
        response = self.client.post(
            reverse("practice:test-start"),
            data=json.dumps({"level": "ielts_8_9", "mode": "paragraph"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["level"], "ielts_8_9")
        self.assertEqual(data["mode"], "paragraph")
        self.assertEqual(data["test_type"], "paragraph")
        self.assertIn("test_id", data)
        self.assertIn("question", data)
        self.assertIn("blanks", data["question"])

    def test_answer_and_retry_paragraph_api(self) -> None:
        start_res = self.client.post(
            reverse("practice:test-start"),
            data=json.dumps({"level": "ielts_8_9", "mode": "paragraph"}),
            content_type="application/json",
        )
        start_data = start_res.json()
        test_id = start_data["test_id"]
        self.assertEqual(start_data["level"], "ielts_8_9")
        self.assertEqual(start_data["mode"], "paragraph")

        # Submit answer for the paragraph
        blanks = start_data["question"]["blanks"]
        answers = {str(b["blank_id"]): "A" for b in blanks}

        answer_res = self.client.post(
            reverse("practice:test-answer", kwargs={"test_id": test_id}),
            data=json.dumps({"answers": answers}),
            content_type="application/json",
        )
        self.assertEqual(answer_res.status_code, 200)
        ans_data = answer_res.json()
        self.assertTrue(ans_data["ok"])
        self.assertEqual(ans_data["mode"], "paragraph")
        self.assertIn("feedback", ans_data)
        self.assertIn("blanks_feedback", ans_data["feedback"])
        self.assertIn("paragraph_explanation", ans_data["feedback"])

        # Retry with different mode or level
        retry_res = self.client.post(
            reverse("practice:test-retry", kwargs={"test_id": test_id}),
            data=json.dumps({"level": "beginner", "mode": "paragraph"}),
            content_type="application/json",
        )
        self.assertEqual(retry_res.status_code, 200)
        retry_data = retry_res.json()
        self.assertTrue(retry_data["ok"])
        self.assertEqual(retry_data["level"], "beginner")
        self.assertEqual(retry_data["mode"], "paragraph")


class ModelAndAITests(TestCase):
    def test_paragraph_bank_seeding_and_levels(self) -> None:
        ParagraphBankQuestion.objects.all().delete()
        created = ParagraphBankQuestion.seed_from_static_bank()
        self.assertGreaterEqual(created, 12)

        beginner_count = ParagraphBankQuestion.objects.filter(level="beginner").count()
        intermediate_count = ParagraphBankQuestion.objects.filter(level="intermediate").count()
        advanced_count = ParagraphBankQuestion.objects.filter(level="advanced").count()
        ielts_count = ParagraphBankQuestion.objects.filter(level="ielts_8_9").count()

        self.assertGreaterEqual(beginner_count, 3)
        self.assertGreaterEqual(intermediate_count, 3)
        self.assertGreaterEqual(advanced_count, 3)
        self.assertGreaterEqual(ielts_count, 3)

    def test_question_bank_seeding_and_ielts_count(self) -> None:
        QuestionBankQuestion.objects.all().delete()
        created = QuestionBankQuestion.seed_from_static_bank()
        self.assertGreaterEqual(created, 45)

        ielts_count = QuestionBankQuestion.objects.filter(level="ielts_8_9").count()
        self.assertGreaterEqual(ielts_count, 12)

    def test_paragraph_random_sample_ielts(self) -> None:
        ParagraphBankQuestion.seed_from_static_bank()
        sampled = ParagraphBankQuestion.random_sample(2, level="ielts_8_9")
        self.assertEqual(len(sampled), 2)
        for item in sampled:
            self.assertEqual(item.level, "ielts_8_9")

    def test_paragraph_blueprint_validation(self) -> None:
        valid_item = {
            "title": "Urban Parks",
            "level": "ielts_8_9",
            "text_with_blanks": "Parks provide fresh air [1] they reduce stress. Many residents [2] there daily.",
            "full_text": "Parks provide fresh air because they reduce stress. Many residents walk there daily.",
            "paragraph_explanation": "Paragraph Building: uses cause conjunctions and present tense consistency.",
            "blanks": [
                {
                    "blank_id": 1,
                    "topic": "Conjunctions",
                    "correct_answer": "because",
                    "distractors": ["so", "but", "unless", "if"],
                    "rule": "Use because to give reason.",
                    "explanation": "Because introduces reason.",
                },
                {
                    "blank_id": 2,
                    "topic": "Subject-verb agreement",
                    "correct_answer": "walk",
                    "distractors": ["walks", "walking", "walked", "is walk"],
                    "rule": "Plural subject takes plural verb.",
                    "explanation": "Many residents is plural.",
                },
            ],
        }

        bp = _validate_paragraph(valid_item)
        self.assertEqual(bp.title, "Urban Parks")
        self.assertEqual(bp.level, "ielts_8_9")
        self.assertEqual(len(bp.blanks), 2)
        self.assertEqual(bp.blanks[0].correct_answer, "because")
        self.assertEqual(len(bp.blanks[0].distractors), 4)

    def test_test_session_mode_persistence(self) -> None:
        p_state = create_paragraph_test_state(total_paragraphs=2, level="ielts_8_9")
        session = TestSession.create_from_state(p_state)
        self.assertEqual(session.test_type, "paragraph")
        self.assertEqual(session.level, "ielts_8_9")

        restored_state = session.to_state()
        self.assertEqual(restored_state["test_type"], "paragraph")
        self.assertEqual(restored_state["mode"], "paragraph")
        self.assertEqual(restored_state["level"], "ielts_8_9")


class VocabularyRepositoryAndAPITests(TestCase):
    def test_vocabulary_repo_loads_datasets(self) -> None:
        from .vocabulary import vocabulary_repo

        vocabulary_repo.ensure_loaded()
        self.assertGreaterEqual(len(vocabulary_repo.oxford_words), 1900)
        self.assertGreaterEqual(len(vocabulary_repo.academic_families), 1900)
        self.assertGreaterEqual(len(vocabulary_repo.academic_entries), 7000)

    def test_vocabulary_sampling_levels_and_modes(self) -> None:
        from .vocabulary import vocabulary_repo

        for lvl in ["beginner", "intermediate", "advanced", "ielts_8_9", "all"]:
            oxford_sample = vocabulary_repo.get_oxford_sample(level=lvl, count=5)
            self.assertEqual(len(oxford_sample), 5)

            academic_sample = vocabulary_repo.get_academic_sample(level=lvl, count=4)
            self.assertEqual(len(academic_sample), 4)

            prompt_sentence = vocabulary_repo.format_prompt_vocabulary_context(level=lvl, count=5, mode="sentence")
            self.assertIn("Source Vocabulary & Lexicon", prompt_sentence)

            prompt_para = vocabulary_repo.format_prompt_vocabulary_context(level=lvl, count=5, mode="paragraph")
            self.assertIn("Source Academic Vocabulary & Word Families", prompt_para)

    def test_vocabulary_lookup_functionality(self) -> None:
        from .vocabulary import vocabulary_repo

        res_ox = vocabulary_repo.lookup_word("scrutiny")
        self.assertIsNotNone(res_ox["oxford"])
        self.assertEqual(res_ox["oxford"]["word"].lower(), "scrutiny")

        res_avl = vocabulary_repo.lookup_word("developmental")
        self.assertTrue(len(res_avl["academic_entries"]) > 0)
        self.assertEqual(res_avl["academic_entries"][0]["family"], "develop")

    def test_ai_prompts_include_vocabulary_context(self) -> None:
        from .ai import _paragraph_prompt, _prompt

        p_sentence = _prompt(total_questions=10, level="advanced")
        self.assertEqual(len(p_sentence), 2)
        user_content_s = p_sentence[1]["content"]
        self.assertIn("Vocabulary & Lexicon Grounding:", user_content_s)
        self.assertIn("Oxford 5000", user_content_s)
        self.assertIn("Academic Vocabulary List", user_content_s)

        p_para = _paragraph_prompt(count=3, level="ielts_8_9")
        self.assertEqual(len(p_para), 2)
        user_content_p = p_para[1]["content"]
        self.assertIn("Thematic Academic Vocabulary & Word Families Context", user_content_p)
        self.assertIn("Academic Vocabulary List", user_content_p)

    def test_vocabulary_sample_api_endpoint(self) -> None:
        response = self.client.get(reverse("practice:vocabulary-sample") + "?level=intermediate&mode=sentence&count=6")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["level"], "intermediate")
        self.assertEqual(data["mode"], "sentence")
        self.assertIn("context_prompt", data)
        self.assertIn("oxford_words", data)
        self.assertIn("academic_families", data)
        self.assertEqual(len(data["oxford_words"]), 6)
        self.assertGreaterEqual(len(data["academic_families"]), 3)

    def test_vocabulary_lookup_api_endpoint(self) -> None:
        response = self.client.get(reverse("practice:vocabulary-lookup") + "?q=research")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["query"], "research")
        self.assertTrue(len(data["academic_entries"]) > 0 or data["oxford"] is not None)

        err_response = self.client.get(reverse("practice:vocabulary-lookup"))
        self.assertEqual(err_response.status_code, 400)
        self.assertFalse(err_response.json()["ok"])
