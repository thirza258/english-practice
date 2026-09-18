from __future__ import annotations

import json
import os
import xml.etree.ElementTree as ET
from dataclasses import replace
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from . import nlp
from .ai import (
    _validate_paragraph,
    _validate_question,
    _validate_writing_report,
    _writing_prompt,
)
from .models import (
    ParagraphBankQuestion,
    QuestionBankQuestion,
    TestSession,
    WritingPromptBankQuestion,
)
from .question_bank import PARAGRAPH_BANK, QUESTION_BANK, ParagraphBlueprint, QuestionBlueprint
from .services import (
    SUPPORTED_MODES,
    build_results,
    create_paragraph_test_state,
    create_test_state,
    create_writing_test_state,
    current_question_payload,
    normalize_level,
    normalize_mode,
    public_paragraph_payload,
    public_question_payload,
    submit_answer,
)
from .writing_bank import WRITING_PROMPT_BANK


class PracticePageTests(TestCase):
    def test_landing_page_has_seo_and_level_links(self) -> None:
        response = self.client.get(reverse("practice:landing"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Learn English. Write with confidence.")
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
        self.assertContains(response, "https://english.nevatal.id/courses/")
        self.assertContains(response, "https://english.nevatal.id/test/")
        self.assertContains(response, "https://english.nevatal.id/test/?mode=paragraph")
        self.assertContains(response, "https://english.nevatal.id/test/?mode=sentence")
        self.assertContains(response, "https://english.nevatal.id/test/?mode=writing")
        self.assertContains(response, "https://english.nevatal.id/test/?mode=paragraph&amp;level=all")
        self.assertContains(response, "https://english.nevatal.id/test/?mode=writing&amp;level=ielts_8_9")
        self.assertContains(response, "<urlset")

        # Verify XML structure and well-formedness
        root = ET.fromstring(response.content)
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = root.findall("s:url", ns)
        self.assertGreaterEqual(len(urls), 36)
        for url in urls:
            self.assertIsNotNone(url.find("s:loc", ns))
            self.assertIsNotNone(url.find("s:lastmod", ns))
            self.assertIsNotNone(url.find("s:changefreq", ns))
            self.assertIsNotNone(url.find("s:priority", ns))


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
        wrong_choice = "B" if state["questions"][1]["correct_answer"] == "A" else "A"
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


class WritingAnalyzerTests(TestCase):
    """The local measurements the model is never asked to make."""

    WEAK = (
        "i think working from home is good. it is good because you save time. many people say it is "
        "good for them. but some people say it is bad because they feel alone. i think the good things "
        "are more than the bad things so companies should let people work from home"
    )

    STRONG = (
        "The proportion of employees working remotely has risen sharply, and opinion remains divided "
        "over whether this development is beneficial.\n\n"
        "The clearest benefit is the time reclaimed from commuting. Employees who previously spent two "
        "hours travelling can devote that period to rest, which tends to improve wellbeing. "
        "Furthermore, organisations that reduce office space obtain substantial savings.\n\n"
        "Nevertheless, the drawbacks should not be dismissed. Informal conversation, which frequently "
        "generates new ideas, is difficult to reproduce remotely. Junior staff may be disadvantaged, "
        "since they acquire professional judgement by observing colleagues.\n\n"
        "On balance, however, these problems appear soluble. Were companies to combine remote work with "
        "regular meetings, the collaborative losses would largely be offset."
    )

    def test_counts_words_sentences_and_paragraphs(self) -> None:
        metrics = nlp.analyze_writing(self.STRONG, min_words=180)

        self.assertGreater(metrics["word_count"], 100)
        self.assertGreater(metrics["sentence_count"], 5)
        self.assertEqual(metrics["paragraph_count"], 4)
        self.assertEqual(metrics["min_words"], 180)

    def test_strong_writing_outscores_weak_writing(self) -> None:
        weak = nlp.analyze_writing(self.WEAK, min_words=180)
        strong = nlp.analyze_writing(self.STRONG, min_words=180)

        self.assertGreater(strong["beyond_core_ratio"], weak["beyond_core_ratio"])
        self.assertGreater(strong["root_type_token_ratio"], weak["root_type_token_ratio"])
        self.assertGreater(
            strong["local_bands"]["lexical_resource"],
            weak["local_bands"]["lexical_resource"],
        )
        self.assertGreater(
            strong["local_bands"]["coherence_cohesion"],
            weak["local_bands"]["coherence_cohesion"],
        )

    def test_detects_repetition_linkers_and_mechanics(self) -> None:
        weak = nlp.analyze_writing(self.WEAK, min_words=180)
        strong = nlp.analyze_writing(self.STRONG, min_words=180)

        self.assertTrue(any(item["word"] == "good" for item in weak["overused_words"]))
        self.assertTrue(any(item["basic"] == "good" for item in weak["basic_word_upgrades"]))
        self.assertTrue(weak["mechanics_issues"])

        self.assertIn("contrast", strong["linker_groups_used"])
        self.assertIn("conclusion", strong["linker_groups_used"])
        self.assertTrue(strong["has_conclusion_signal"])
        self.assertTrue(strong["academic_words_used"])

    def test_referencing_counts_as_cohesion(self) -> None:
        """Higher-band writing links ideas by referencing, not only by connectives."""

        referencing = (
            "Remote work reduces commuting time. This saving is substantial for many employees. "
            "Such arrangements also cut office costs, and those savings can fund training. "
            "The former benefits the individual; the latter benefits the organisation."
        )
        plain = (
            "Remote work reduces commuting time. It saves a lot for many employees. "
            "It also cuts office costs, and money can fund training. "
            "One helps the person and one helps the company."
        )

        with_refs = nlp.analyze_writing(referencing, min_words=100)
        without_refs = nlp.analyze_writing(plain, min_words=100)

        self.assertGreaterEqual(with_refs["referencing_count"], 4)
        self.assertEqual(without_refs["referencing_count"], 0)
        self.assertGreater(
            with_refs["local_bands"]["coherence_cohesion"],
            without_refs["local_bands"]["coherence_cohesion"],
        )
        self.assertIn("refs=", with_refs["digest"])

    def test_digest_is_short_and_carries_the_key_numbers(self) -> None:
        metrics = nlp.analyze_writing(self.STRONG, min_words=180)
        digest = metrics["digest"]

        self.assertLess(len(digest), 400)
        self.assertIn(f"words={metrics['word_count']}", digest)
        self.assertIn("linkers=", digest)
        self.assertNotIn("\n", digest)

    def test_short_and_empty_text_are_handled(self) -> None:
        for text in ("", "   ", "Hello.", "Working from home is good because you save time."):
            metrics = nlp.analyze_writing(text, min_words=250)
            self.assertFalse(metrics["meets_min_words"])
            for score in metrics["local_bands"].values():
                self.assertLessEqual(score, 5.0)

    def test_word_count_does_not_depend_on_nltk(self) -> None:
        """The count drives the length penalty, so it must be identical everywhere.

        It also has to match the live counter in the browser, which uses the same
        pattern. NLTK is used for sentence segmentation only.
        """

        text = "Dr. Smith doesn't agree. He said it's a work-life issue, i.e. a real one."
        metrics = nlp.analyze_writing(text, min_words=100)

        self.assertEqual(metrics["word_count"], len(nlp.WORD_RE.findall(text)))

        with mock.patch.dict(os.environ, {"WRITING_DISABLE_NLTK": "1"}, clear=False):
            nlp._NLTK_SENT = None  # force the probe to run again
            try:
                without_nltk = nlp.analyze_writing(text, min_words=100)
            finally:
                nlp._NLTK_SENT = None

        self.assertEqual(without_nltk["word_count"], metrics["word_count"])

    def test_overall_band_uses_ielts_rounding(self) -> None:
        self.assertEqual(
            nlp.overall_band(
                {
                    "task_response": 6.0,
                    "coherence_cohesion": 6.5,
                    "lexical_resource": 6.5,
                    "grammatical_range": 6.0,
                }
            ),
            6.5,
        )
        self.assertEqual(
            nlp.overall_band(
                {
                    "task_response": 7.0,
                    "coherence_cohesion": 7.0,
                    "lexical_resource": 6.5,
                    "grammatical_range": 6.5,
                }
            ),
            7.0,
        )
        self.assertEqual(nlp.round_half_band(12.4), 9.0)
        self.assertEqual(nlp.round_half_band(-3), 0.0)

    def test_length_penalty_caps_task_response(self) -> None:
        metrics = nlp.analyze_writing(self.STRONG, min_words=400)
        bands, notes = nlp.apply_length_penalty(dict(metrics["local_bands"]), metrics)

        self.assertLessEqual(bands["task_response"], 5.0)
        self.assertTrue(notes)
        self.assertIn("400-word minimum", notes[0])


@mock.patch.dict(os.environ, {"WRITING_AI_ENABLED": "0"}, clear=False)
class WritingModeServiceTests(TestCase):
    """Writing mode end to end with no model configured."""

    ESSAY = (
        "Employers increasingly allow staff to work remotely, and the consequences of this shift "
        "remain contested. Although the arrangement creates genuine difficulties for collaboration, "
        "I would argue that its benefits are considerable when it is designed carefully.\n\n"
        "The principal advantage is the time reclaimed from commuting. Employees who once spent two "
        "hours travelling can devote that period to rest or family, which tends to improve both "
        "wellbeing and productivity. Furthermore, organisations that reduce office space obtain "
        "substantial savings, and these can be redirected towards training.\n\n"
        "Nevertheless, the drawbacks deserve attention. Informal conversation, which frequently "
        "generates new ideas, is difficult to reproduce on a video call. Junior employees in "
        "particular may be disadvantaged, since they acquire professional judgement by observing "
        "experienced colleagues at close quarters. The boundary between working hours and private "
        "life also becomes indistinct when both occupy the same room.\n\n"
        "On balance, however, these difficulties appear soluble. Were companies to combine remote work "
        "with regular meetings in person, the collaborative losses would largely be offset. I would "
        "therefore argue that flexible arrangements ought to be retained, provided that they are "
        "designed deliberately rather than adopted by default."
    )

    def test_normalize_mode_accepts_writing(self) -> None:
        self.assertEqual(normalize_mode("writing"), "writing")
        self.assertEqual(normalize_mode("WRITING"), "writing")
        self.assertIn("writing", SUPPORTED_MODES)

    def test_create_writing_state_for_every_level(self) -> None:
        for level in ["beginner", "intermediate", "advanced", "ielts_8_9", "all"]:
            state = create_writing_test_state(level=level)

            self.assertEqual(state["test_type"], "writing")
            self.assertEqual(state["mode"], "writing")
            self.assertEqual(state["level"], level)
            self.assertEqual(state["total_tasks"], 1)
            self.assertEqual(state["total_questions"], 1)
            self.assertEqual(len(state["questions"]), 1)

            task = state["questions"][0]
            if level != "all":
                self.assertEqual(task["level"], level)
            self.assertTrue(task["title"])
            self.assertTrue(task["prompt"])
            self.assertGreaterEqual(task["min_words"], 80)
            self.assertTrue(task["guidance"])
            self.assertTrue(task["model_outline"])

    def test_public_payload_hides_target_vocabulary_and_outline(self) -> None:
        state = create_writing_test_state(level="advanced")
        payload = current_question_payload(state)

        self.assertIsNotNone(payload)
        self.assertIn("prompt", payload)
        self.assertIn("guidance", payload)
        self.assertNotIn("useful_vocabulary", payload)
        self.assertNotIn("model_outline", payload)
        self.assertNotIn("submission", payload)

    def test_writing_tasks_stay_at_the_requested_level_when_bank_runs_short(self) -> None:
        expected = [item for item in WRITING_PROMPT_BANK if item.level == "beginner"]
        state = create_writing_test_state(total_tasks=len(WRITING_PROMPT_BANK), level="beginner")

        self.assertEqual(state["total_tasks"], len(expected))
        self.assertEqual(state["total_questions"], len(expected))
        self.assertCountEqual(
            [task["prompt"] for task in state["questions"]],
            [item.prompt for item in expected],
        )

    def test_missing_writing_level_does_not_fall_back_to_other_levels(self) -> None:
        bank = [item for item in WRITING_PROMPT_BANK if item.level != "beginner"]
        with mock.patch("practice.writing_bank.WRITING_PROMPT_BANK", bank):
            with self.assertRaisesMessage(ValueError, "No writing prompts"):
                create_writing_test_state(level="beginner")

    def test_submission_produces_a_band_report(self) -> None:
        state = create_writing_test_state(level="intermediate")
        result = submit_answer(state, self.ESSAY)
        feedback = result["feedback"]

        self.assertTrue(result["completed"])
        self.assertEqual(feedback["assessed_by"], "measured")
        self.assertEqual(len(feedback["criteria"]), 4)
        self.assertEqual(
            [criterion["key"] for criterion in feedback["criteria"]],
            list(nlp.CRITERIA),
        )
        for criterion in feedback["criteria"]:
            self.assertGreaterEqual(criterion["band"], 0.0)
            self.assertLessEqual(criterion["band"], 9.0)
            self.assertTrue(criterion["comment"])

        self.assertGreater(feedback["overall_band"], 0)
        self.assertTrue(feedback["strengths"])
        self.assertEqual(feedback["essay"], self.ESSAY)
        self.assertTrue(feedback["metrics"]["word_count"] > 150)
        self.assertTrue(feedback["revealed"]["model_outline"])
        self.assertTrue(feedback["revealed"]["useful_vocabulary"])
        # No model configured, so the local analysis must say so.
        self.assertTrue(any("local analysis" in note for note in feedback["notes"]))

    def test_weak_writing_scores_below_strong_writing(self) -> None:
        weak_state = create_writing_test_state(level="intermediate")
        strong_state = create_writing_test_state(level="intermediate")

        weak_essay = (
            "I think working from home is good. It is good because you save time and money. "
            "Many people say it is good for them. But some people say it is bad because they feel "
            "alone at home. I think the good things are more than the bad things. So companies "
            "should let people work from home if they want to do it."
        )

        weak = submit_answer(weak_state, weak_essay)["feedback"]
        strong = submit_answer(strong_state, self.ESSAY)["feedback"]

        self.assertLess(weak["overall_band"], strong["overall_band"])
        self.assertLess(
            weak["bands"]["lexical_resource"],
            strong["bands"]["lexical_resource"],
        )
        self.assertTrue(weak["improvements"])

    def test_under_length_response_caps_task_response(self) -> None:
        state = create_writing_test_state(level="advanced")
        state["questions"][0]["min_words"] = 250

        short_essay = " ".join(
            [
                "Automation will undoubtedly displace a considerable number of existing roles,",
                "yet the appropriate response is contested. Retraining programmes are frequently",
                "proposed, although their effectiveness remains uncertain in practice.",
            ]
        )
        feedback = submit_answer(state, short_essay)["feedback"]

        self.assertLessEqual(feedback["bands"]["task_response"], 5.0)
        self.assertTrue(any("capped" in note for note in feedback["notes"]))

    def test_invalid_submissions_are_rejected(self) -> None:
        for payload, fragment in (
            (123, "must be sent as text"),
            ({"essay": "x"}, "must be sent as text"),
            ("Too short to mark.", "at least"),
            ("x" * 20001, "too long"),
        ):
            state = create_writing_test_state(level="beginner")
            with self.assertRaises(ValueError) as ctx:
                submit_answer(state, payload)
            self.assertIn(fragment, str(ctx.exception))

    def test_resubmitting_the_same_task_is_rejected(self) -> None:
        state = create_writing_test_state(level="intermediate")
        submit_answer(state, self.ESSAY)

        with self.assertRaises(ValueError):
            submit_answer(state, self.ESSAY)

    def test_results_bypass_the_topic_summary(self) -> None:
        state = create_writing_test_state(level="ielts_8_9")
        submit_answer(state, self.ESSAY)
        results = build_results(state)

        self.assertEqual(results["test_type"], "writing")
        self.assertEqual(results["topic_summary"], [])
        self.assertEqual(len(results["criteria_summary"]), 4)
        self.assertGreater(results["overall_band"], 0)
        self.assertEqual(results["percentage"], round(results["overall_band"] / 9 * 100))
        self.assertEqual(len(results["tasks"]), 1)
        self.assertIn("metrics", results["tasks"][0])
        json.dumps(results)

    def test_session_state_round_trips_through_the_database(self) -> None:
        state = create_writing_test_state(level="advanced")
        submit_answer(state, self.ESSAY)
        session = TestSession.create_from_state(state)

        self.assertEqual(session.test_type, "writing")
        restored = session.to_state()
        self.assertEqual(restored["test_type"], "writing")
        self.assertEqual(restored["questions"][0]["submission"]["essay"], self.ESSAY)
        self.assertTrue(build_results(restored)["overall_band"] > 0)


@mock.patch.dict(os.environ, {"WRITING_AI_ENABLED": "0"}, clear=False)
class WritingApiTests(TestCase):
    def test_start_uses_corrected_prompt_content_from_an_existing_bank(self) -> None:
        corrected = WRITING_PROMPT_BANK[0]
        previous = replace(corrected, prompt="Previous task wording.")
        entry = WritingPromptBankQuestion.from_blueprint(previous)
        entry.save()

        with mock.patch("practice.writing_bank.WRITING_PROMPT_BANK", [corrected]):
            response = self.client.post(
                reverse("practice:test-start"),
                data=json.dumps({"level": corrected.level, "mode": "writing"}),
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 200)
        question = response.json()["question"]
        self.assertEqual(question["prompt"], corrected.prompt)
        self.assertEqual(question["guidance"], list(corrected.guidance))
        self.assertNotIn("model_outline", question)
        self.assertNotIn("useful_vocabulary", question)
        self.assertEqual(WritingPromptBankQuestion.objects.count(), 1)

    def test_writing_test_lifecycle_over_the_api(self) -> None:
        start = self.client.post(
            reverse("practice:test-start"),
            data=json.dumps({"level": "intermediate", "mode": "writing"}),
            content_type="application/json",
        )
        self.assertEqual(start.status_code, 200)
        start_data = start.json()

        self.assertEqual(start_data["mode"], "writing")
        self.assertEqual(start_data["test_type"], "writing")
        self.assertEqual(start_data["total_items"], 1)
        task = start_data["question"]
        self.assertIn("prompt", task)
        self.assertNotIn("model_outline", task)

        essay = WritingModeServiceTests.ESSAY
        answer = self.client.post(
            reverse("practice:test-answer", kwargs={"test_id": start_data["test_id"]}),
            data=json.dumps({"essay": essay}),
            content_type="application/json",
        )
        self.assertEqual(answer.status_code, 200)
        data = answer.json()

        self.assertTrue(data["ok"])
        self.assertEqual(data["mode"], "writing")
        # Regression: the sentence branch used to upper-case and discard the body.
        self.assertEqual(data["feedback"]["essay"], essay)
        self.assertIn("criteria", data["feedback"])
        self.assertIn("results", data)
        self.assertGreater(data["results"]["overall_band"], 0)

    def test_short_submission_returns_a_readable_error(self) -> None:
        start = self.client.post(
            reverse("practice:test-start"),
            data=json.dumps({"level": "beginner", "mode": "writing"}),
            content_type="application/json",
        ).json()

        response = self.client.post(
            reverse("practice:test-answer", kwargs={"test_id": start["test_id"]}),
            data=json.dumps({"essay": "Too short."}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("at least", response.json()["error"])

    def test_retry_can_switch_into_writing_mode(self) -> None:
        start = self.client.post(
            reverse("practice:test-start"),
            data=json.dumps({"level": "all", "mode": "sentence"}),
            content_type="application/json",
        ).json()

        retry = self.client.post(
            reverse("practice:test-retry", kwargs={"test_id": start["test_id"]}),
            data=json.dumps({"level": "advanced", "mode": "writing"}),
            content_type="application/json",
        )

        self.assertEqual(retry.status_code, 200)
        data = retry.json()
        self.assertEqual(data["mode"], "writing")
        self.assertEqual(data["level"], "advanced")
        self.assertIn("prompt", data["question"])

    def test_completed_writing_session_is_restored_on_the_page(self) -> None:
        start = self.client.post(
            reverse("practice:test-start"),
            data=json.dumps({"level": "intermediate", "mode": "writing"}),
            content_type="application/json",
        ).json()
        self.client.post(
            reverse("practice:test-answer", kwargs={"test_id": start["test_id"]}),
            data=json.dumps({"essay": WritingModeServiceTests.ESSAY}),
            content_type="application/json",
        )

        page = self.client.get(reverse("practice:test") + "?mode=writing")

        self.assertEqual(page.status_code, 200)
        self.assertContains(page, "initial-state-data")
        self.assertContains(page, "initial-results-data")

        results = self.client.get(
            reverse("practice:test-results", kwargs={"test_id": start["test_id"]})
        )
        self.assertEqual(results.status_code, 200)
        self.assertGreater(results.json()["overall_band"], 0)

    def test_pages_expose_the_writing_mode(self) -> None:
        landing = self.client.get(reverse("practice:landing"))
        self.assertContains(landing, f'{reverse("practice:test")}?mode=writing&level=all')
        self.assertContains(landing, f'{reverse("practice:test")}?mode=writing&level=ielts_8_9')

        page = self.client.get(reverse("practice:test") + "?mode=writing&level=advanced")
        self.assertContains(page, 'requestedMode: "writing"')
        self.assertContains(page, 'data-mode="writing"')


class WritingEvaluationPromptTests(TestCase):
    """The request stays small and the reply is validated before use."""

    METRICS_DIGEST = (
        "words=212 sents=13 paras=4 | rttr=9.8 beyond_core=0.52 academic=7 long=0.24 | "
        "avg_sent=16.3 sd=5.1 complex=0.62 compound=0.15 passive=3 | linkers=cause,contrast,conclusion"
    )
    LOCAL_BANDS = {
        "task_response": 6.5,
        "coherence_cohesion": 7.0,
        "lexical_resource": 7.5,
        "grammatical_range": 7.0,
    }

    def _prompt(self, essay: str) -> list[dict[str, str]]:
        return _writing_prompt(
            essay=essay,
            digest=self.METRICS_DIGEST,
            local_bands=self.LOCAL_BANDS,
            task_title="Working From Home",
            task_prompt="Discuss the advantages and disadvantages of remote work.",
            level="advanced",
        )

    def test_prompt_sends_the_digest_instead_of_raw_statistics(self) -> None:
        messages = self._prompt("A short response about remote work. " * 10)
        user = messages[1]["content"]

        self.assertEqual(messages[0]["role"], "system")
        self.assertIn(self.METRICS_DIGEST, user)
        self.assertIn("Working From Home", user)
        self.assertIn("task_response=6.5", user)
        # The whole request stays compact: no metric dump, no descriptor text.
        self.assertLess(len(user), 4000)
        self.assertNotIn("linkers_by_group", user)

    def test_long_essays_are_truncated(self) -> None:
        essay = " ".join(["consideration"] * 900)
        user = self._prompt(essay)[1]["content"]

        self.assertIn("[...truncated]", user)
        self.assertLess(user.count("consideration"), 900)

    def test_report_validation_normalises_the_short_key_shape(self) -> None:
        report = _validate_writing_report(
            {
                "tr": [6.4, "  Addresses both sides   but the conclusion is thin.  "],
                "cc": [7, "Clear paragraphing."],
                "lr": {"band": "7.5", "comment": "Precise, varied lexis."},
                "gra": [12, "Accurate."],
                "str": ["Strong topic sentences", "", "Good range of linkers"],
                "imp": ["Develop the second body paragraph"],
                "fix": [
                    {"o": "the datas show", "c": "the data show", "w": "data is plural"},
                    {"o": "", "c": "dropped because it has no original"},
                ],
                "voc": [
                    {"b": "good", "u": "beneficial, advantageous"},
                    {"b": "", "u": "dropped"},
                ],
            }
        )

        self.assertEqual(report["bands"]["task_response"], 6.5)
        self.assertEqual(report["bands"]["coherence_cohesion"], 7.0)
        self.assertEqual(report["bands"]["lexical_resource"], 7.5)
        self.assertEqual(report["bands"]["grammatical_range"], 9.0)
        self.assertEqual(
            report["comments"]["task_response"],
            "Addresses both sides but the conclusion is thin.",
        )
        self.assertEqual(report["strengths"], ["Strong topic sentences", "Good range of linkers"])
        self.assertEqual(len(report["corrections"]), 1)
        self.assertEqual(report["corrections"][0]["original"], "the datas show")
        self.assertEqual(len(report["vocabulary_upgrades"]), 1)

    def test_missing_bands_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            _validate_writing_report({"tr": [6.0, "ok"], "cc": [6.0, "ok"], "lr": [6.0, "ok"]})


class WritingPromptBankTests(TestCase):
    def test_bank_seeds_every_level(self) -> None:
        WritingPromptBankQuestion.objects.all().delete()
        created = WritingPromptBankQuestion.seed_from_static_bank()

        self.assertEqual(created, len(WRITING_PROMPT_BANK))
        for level in ("beginner", "intermediate", "advanced", "ielts_8_9"):
            self.assertGreaterEqual(
                WritingPromptBankQuestion.objects.filter(level=level).count(),
                5,
                f"too few {level} writing prompts",
            )

    def test_seeding_is_idempotent(self) -> None:
        WritingPromptBankQuestion.seed_from_static_bank()
        before = WritingPromptBankQuestion.objects.count()
        WritingPromptBankQuestion.seed_from_static_bank()

        self.assertEqual(WritingPromptBankQuestion.objects.count(), before)

    def test_reseeding_refreshes_task_details_without_replacing_the_prompt(self) -> None:
        WritingPromptBankQuestion.seed_from_static_bank()
        original = WRITING_PROMPT_BANK[0]
        entry = WritingPromptBankQuestion.objects.get(title=original.title)
        updated = replace(
            original,
            task_type="narrative",
            min_words=100,
            suggested_minutes=25,
            guidance=("Explain what happened and how you felt.",),
            useful_vocabulary=("afterwards", "eventually"),
            model_outline="Describe the events, then reflect on the day.",
        )

        with mock.patch("practice.writing_bank.WRITING_PROMPT_BANK", [updated]):
            created = WritingPromptBankQuestion.seed_from_static_bank()

        entry.refresh_from_db()
        self.assertEqual(created, 0)
        self.assertEqual(WritingPromptBankQuestion.objects.count(), len(WRITING_PROMPT_BANK))
        self.assertEqual(entry.to_blueprint(), updated)

    def test_reseeding_preserves_custom_prompt_details(self) -> None:
        custom = replace(WRITING_PROMPT_BANK[0], min_words=120, guidance=("Custom guidance.",))
        entry = WritingPromptBankQuestion.from_blueprint(
            custom, source="custom", generation_metadata={"note": "teacher supplied"}
        )
        entry.save()

        WritingPromptBankQuestion.seed_from_static_bank()

        entry.refresh_from_db()
        self.assertEqual(entry.to_blueprint(), custom)
        self.assertEqual(entry.source, "custom")
        self.assertEqual(entry.generation_metadata, {"note": "teacher supplied"})

    def test_reseeding_updates_prompt_wording_in_place(self) -> None:
        corrected = WRITING_PROMPT_BANK[0]
        entry = WritingPromptBankQuestion.from_blueprint(
            replace(corrected, prompt="Previous task wording.")
        )
        entry.save()
        old_hash = entry.content_hash

        with mock.patch("practice.writing_bank.WRITING_PROMPT_BANK", [corrected]):
            self.assertEqual(WritingPromptBankQuestion.seed_from_static_bank(), 0)
            self.assertEqual(WritingPromptBankQuestion.seed_from_static_bank(), 0)

        entry.refresh_from_db()
        self.assertEqual(entry.to_blueprint(), corrected)
        self.assertNotEqual(entry.content_hash, old_hash)
        self.assertEqual(WritingPromptBankQuestion.objects.count(), 1)
        self.assertFalse(WritingPromptBankQuestion.objects.filter(content_hash=old_hash).exists())

    def test_reseeding_does_not_replace_a_custom_prompt_with_the_same_title(self) -> None:
        corrected = WRITING_PROMPT_BANK[0]
        custom = replace(corrected, prompt="A teacher's own version of this task.")
        entry = WritingPromptBankQuestion.from_blueprint(custom, source="custom")
        entry.save()

        with mock.patch("practice.writing_bank.WRITING_PROMPT_BANK", [corrected]):
            self.assertEqual(WritingPromptBankQuestion.seed_from_static_bank(), 1)

        entry.refresh_from_db()
        self.assertEqual(entry.to_blueprint(), custom)
        self.assertEqual(entry.source, "custom")
        self.assertEqual(WritingPromptBankQuestion.objects.count(), 2)

    def test_blueprint_round_trip(self) -> None:
        WritingPromptBankQuestion.seed_from_static_bank()
        entry = WritingPromptBankQuestion.objects.filter(level="ielts_8_9").first()
        blueprint = entry.to_blueprint()

        self.assertEqual(blueprint.level, "ielts_8_9")
        self.assertGreaterEqual(blueprint.min_words, 250)
        self.assertTrue(blueprint.guidance)
        self.assertTrue(blueprint.useful_vocabulary)
        self.assertTrue(blueprint.model_outline)

    def test_random_sample_respects_the_level(self) -> None:
        WritingPromptBankQuestion.seed_from_static_bank()
        sampled = WritingPromptBankQuestion.random_sample(3, level="beginner")

        self.assertEqual(len(sampled), 3)
        for item in sampled:
            self.assertEqual(item.level, "beginner")

    def test_random_sample_does_not_fill_shortfall_from_other_levels(self) -> None:
        WritingPromptBankQuestion.seed_from_static_bank()
        expected = WritingPromptBankQuestion.objects.filter(level="beginner")

        sampled = WritingPromptBankQuestion.random_sample(len(WRITING_PROMPT_BANK), level="BEGINNER")

        self.assertCountEqual([item.pk for item in sampled], expected.values_list("pk", flat=True))

    def test_random_sample_returns_empty_when_all_matching_prompts_are_excluded(self) -> None:
        WritingPromptBankQuestion.seed_from_static_bank()
        excluded = WritingPromptBankQuestion.objects.filter(level="beginner").values_list(
            "content_hash", flat=True
        )

        sampled = WritingPromptBankQuestion.random_sample(3, level="beginner", exclude_hashes=excluded)

        self.assertEqual(sampled, [])

    def test_random_sample_all_levels_returns_each_prompt_at_most_once(self) -> None:
        WritingPromptBankQuestion.seed_from_static_bank()

        sampled = WritingPromptBankQuestion.random_sample(len(WRITING_PROMPT_BANK) + 1, level="all")

        self.assertEqual(len(sampled), len(WRITING_PROMPT_BANK))
        self.assertEqual(len({item.pk for item in sampled}), len(sampled))


@mock.patch.dict(
    os.environ,
    {"WRITING_AI_ENABLED": "1", "OPENROUTER_API_KEY": "test-key"},
    clear=False,
)
class WritingExaminerMergeTests(TestCase):
    """How an examiner reply is combined with the local measurements."""

    EXAMINER_REPLY = {
        "bands": {
            "task_response": 8.0,
            "coherence_cohesion": 7.5,
            "lexical_resource": 8.0,
            "grammatical_range": 7.5,
        },
        "comments": {
            "task_response": "Both sides are addressed with a clear position.",
            "coherence_cohesion": "Logical paragraphing throughout.",
            "lexical_resource": "Precise and varied lexis.",
            "grammatical_range": "A wide range of accurate structures.",
        },
        "strengths": ["Clear thesis", "Well-chosen examples"],
        "improvements": ["Develop the counter-argument further"],
        "corrections": [
            {"original": "the datas show", "corrected": "the data show", "why": "data is plural"}
        ],
        "vocabulary_upgrades": [{"basic": "important", "stronger": "pivotal, decisive"}],
        "usage": {"prompt_tokens": 480, "completion_tokens": 260, "total_tokens": 740},
        "model": "openai/gpt-4o-mini",
    }

    def test_examiner_bands_are_used_and_measurements_are_kept(self) -> None:
        state = create_writing_test_state(level="intermediate")
        essay = WritingModeServiceTests.ESSAY

        with mock.patch(
            "practice.services.evaluate_writing",
            return_value=dict(self.EXAMINER_REPLY),
        ) as evaluator:
            feedback = submit_answer(state, essay)["feedback"]

        call = evaluator.call_args.kwargs
        self.assertEqual(call["essay"], essay)
        self.assertIn("words=", call["digest"])
        self.assertEqual(set(call["local_bands"]), set(nlp.CRITERIA))
        self.assertTrue(call["task_prompt"])

        self.assertEqual(feedback["assessed_by"], "examiner")
        self.assertEqual(feedback["bands"]["lexical_resource"], 8.0)
        self.assertEqual(feedback["overall_band"], 8.0)
        self.assertEqual(feedback["strengths"], ["Clear thesis", "Well-chosen examples"])
        self.assertEqual(feedback["model"], "openai/gpt-4o-mini")
        self.assertEqual(feedback["usage"]["total_tokens"], 740)

        # The measured view survives alongside the examiner's. A strong response
        # can legitimately leave nothing for the local analysis to flag.
        self.assertTrue(feedback["measured_bands"])
        self.assertIsInstance(feedback["measured_observations"], list)
        for criterion in feedback["criteria"]:
            self.assertIn("measured_band", criterion)
        self.assertTrue(feedback["metrics"]["word_count"] > 150)

        # Examiner suggestions rank ahead of measured ones, with no duplicates.
        upgrades = feedback["vocabulary_upgrades"]
        self.assertEqual(upgrades[0]["basic"], "important")
        self.assertEqual(upgrades[0]["source"], "examiner")
        self.assertEqual(len({item["basic"].lower() for item in upgrades}), len(upgrades))

    def test_measured_observations_accompany_the_examiner_review(self) -> None:
        state = create_writing_test_state(level="intermediate")
        weak_essay = (
            "I think working from home is good. It is good because you save time and money. "
            "Many people say it is good for them. But some people say it is bad because they "
            "feel alone at home. I think the good things are more than the bad things. So "
            "companies should let people work from home if they really want to do it."
        )

        with mock.patch("practice.services.evaluate_writing", return_value=dict(self.EXAMINER_REPLY)):
            feedback = submit_answer(state, weak_essay)["feedback"]

        self.assertEqual(feedback["assessed_by"], "examiner")
        self.assertTrue(feedback["measured_observations"])
        self.assertTrue(any("good" in item for item in feedback["measured_observations"]))
        self.assertTrue(any(item["source"] == "measured" for item in feedback["vocabulary_upgrades"]))

    def test_length_penalty_overrides_a_generous_examiner(self) -> None:
        state = create_writing_test_state(level="advanced")
        state["questions"][0]["min_words"] = 250

        # Long enough to reach the examiner, far short of the 250-word minimum.
        short_essay = (
            "Automation will displace a considerable number of existing roles, yet the appropriate "
            "response remains contested. Retraining programmes are frequently proposed, although "
            "their effectiveness is uncertain and their cost substantial. Some economists argue that "
            "the productivity gains should instead be redistributed, since displaced workers rarely "
            "return to equivalent employment. Governments should therefore proceed cautiously, "
            "weighing the transitional damage against the long-term benefit."
        )

        with mock.patch("practice.services.evaluate_writing", return_value=dict(self.EXAMINER_REPLY)):
            feedback = submit_answer(state, short_essay)["feedback"]

        self.assertEqual(feedback["assessed_by"], "examiner")
        self.assertLessEqual(feedback["bands"]["task_response"], 5.0)
        self.assertTrue(any("capped" in note for note in feedback["notes"]))

    def test_examiner_failure_falls_back_to_the_local_report(self) -> None:
        state = create_writing_test_state(level="intermediate")

        with mock.patch(
            "practice.services.evaluate_writing",
            side_effect=RuntimeError("connection reset"),
        ):
            feedback = submit_answer(state, WritingModeServiceTests.ESSAY)["feedback"]

        self.assertEqual(feedback["assessed_by"], "measured")
        self.assertIn("connection reset", feedback["ai_error"])
        self.assertEqual(feedback["bands"], feedback["measured_bands"])
        self.assertTrue(feedback["strengths"])
        self.assertTrue(any("could not be reached" in note for note in feedback["notes"]))

    def test_very_short_response_never_calls_the_model(self) -> None:
        state = create_writing_test_state(level="beginner")
        # Above the submission floor, below the threshold for an examiner review.
        essay = (
            "Working from home saves a lot of time for many people today. It is good "
            "because you do not travel. But it can also be lonely sometimes."
        )

        with mock.patch("practice.services.evaluate_writing") as evaluator:
            feedback = submit_answer(state, essay)["feedback"]

        evaluator.assert_not_called()
        self.assertEqual(feedback["assessed_by"], "measured")
        self.assertTrue(any("scored locally only" in note for note in feedback["notes"]))
