from __future__ import annotations

import os
import random
import re
import uuid
from typing import Any

from . import nlp
from .ai import evaluate_writing, generate_paragraph_blueprints, generate_question_blueprints
from .models import (
    ParagraphBankQuestion,
    QuestionBankQuestion,
    TestSession,
    WritingPromptBankQuestion,
)
from .question_bank import ParagraphBlueprint, QuestionBlueprint
from .writing_bank import WritingPromptBlueprint


LETTERS = ["A", "B", "C", "D", "E"]
TEST_SESSION_KEY = "english_practice_active_test"
SUPPORTED_LEVELS = ("all", "beginner", "intermediate", "advanced", "ielts_8_9")
SUPPORTED_MODES = ("sentence", "paragraph", "writing")


def normalize_level(level: str | None) -> str:
    if not level:
        return "all"
    cleaned = str(level).strip().lower()
    if cleaned in ("ielts", "ielts_8_9", "ielts-8-9", "ielts 8-9", "ielts89", "band89", "band_8_9", "ielts_89"):
        return "ielts_8_9"
    return cleaned if cleaned in SUPPORTED_LEVELS else "all"



def normalize_mode(mode: str | None) -> str:
    if not mode:
        return "sentence"
    cleaned = str(mode).strip().lower()
    return cleaned if cleaned in SUPPORTED_MODES else "sentence"


def _randomizer() -> random.Random:
    return random.SystemRandom()


def _ensure_seeded_bank() -> None:
    QuestionBankQuestion.seed_from_static_bank()
    ParagraphBankQuestion.seed_from_static_bank()
    WritingPromptBankQuestion.seed_from_static_bank()


def _lettered_options(options: list[str]) -> list[dict[str, str]]:
    return [{"label": label, "text": text} for label, text in zip(LETTERS, options, strict=True)]


def _format_choice(label: str, text: str) -> str:
    return f"{label}. {text}"


# -----------------------------------------------------------------------------
# SENTENCE MODE SERVICES
# -----------------------------------------------------------------------------

def _build_question(blueprint: QuestionBlueprint, question_number: int, rng: random.Random) -> dict[str, Any]:
    options = [blueprint.correct_answer, *blueprint.distractors]
    rng.shuffle(options)
    correct_index = options.index(blueprint.correct_answer)
    correct_letter = LETTERS[correct_index]

    return {
        "id": f"q{question_number}",
        "question_number": question_number,
        "question": blueprint.question,
        "options": _lettered_options(options),
        "correct_answer": correct_letter,
        "correct_answer_text": blueprint.correct_answer,
        "grammar_topic": blueprint.topic,
        "grammar_topics": [blueprint.topic, *blueprint.secondary_topics],
        "level": blueprint.level,
        "rule": blueprint.rule,
        "explanation": blueprint.explanation,
        "sentence_explanation": blueprint.sentence_explanation,
        "selected_answer": None,
        "is_correct": None,
    }


def _generated_blueprints(total_questions: int, level: str = "all") -> list[QuestionBlueprint]:
    _ensure_seeded_bank()
    normalized_level = normalize_level(level)

    bank_count = (
        QuestionBankQuestion.objects.filter(level=normalized_level).count()
        if normalized_level != "all"
        else QuestionBankQuestion.objects.count()
    )
    generate_count = total_questions if bank_count < 500 else min(5, total_questions)

    generated: list[QuestionBlueprint] = []
    if generate_count > 0:
        try:
            generated = generate_question_blueprints(generate_count, level=normalized_level)
        except Exception:
            generated = []

    if generated:
        QuestionBankQuestion.save_blueprints(
            generated,
            source="openrouter",
            generation_metadata={"bank_size_before": bank_count, "requested_level": normalized_level},
        )

    if bank_count >= 500:
        sampled_count = total_questions - len(generated)
        exclude_hashes = {
            QuestionBankQuestion.fingerprint(
                topic=blueprint.topic,
                question=blueprint.question,
                correct_answer=blueprint.correct_answer,
                distractors=blueprint.distractors,
                secondary_topics=blueprint.secondary_topics,
                level=blueprint.level,
            )
            for blueprint in generated
        }
        sampled_entries = QuestionBankQuestion.random_sample(
            sampled_count,
            level=normalized_level if normalized_level != "all" else None,
            exclude_hashes=exclude_hashes,
        )
        if len(sampled_entries) < sampled_count:
            sampled_entries = QuestionBankQuestion.random_sample(
                sampled_count,
                level=normalized_level if normalized_level != "all" else None,
            )

        combined = [*generated, *(entry.to_blueprint() for entry in sampled_entries)]
        rng = _randomizer()
        rng.shuffle(combined)
        return combined

    if generated:
        return generated

    sampled_entries = QuestionBankQuestion.random_sample(
        total_questions,
        level=normalized_level if normalized_level != "all" else None,
    )
    if len(sampled_entries) < total_questions:
        raise ValueError("Not enough questions in the bank to build a test.")
    return [entry.to_blueprint() for entry in sampled_entries]


def create_test_state(total_questions: int = 10, level: str = "all") -> dict[str, Any]:
    rng = _randomizer()
    normalized_level = normalize_level(level)
    selected_blueprints = _generated_blueprints(total_questions, level=normalized_level)
    questions = [_build_question(blueprint, index + 1, rng) for index, blueprint in enumerate(selected_blueprints)]

    return {
        "id": uuid.uuid4().hex,
        "test_type": "sentence",
        "mode": "sentence",
        "level": normalized_level,
        "total_questions": total_questions,
        "current_index": 0,
        "score": 0,
        "completed": False,
        "questions": questions,
    }


def public_question_payload(question: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": question["id"],
        "question_number": question["question_number"],
        "question": question["question"],
        "options": question["options"],
    }


# -----------------------------------------------------------------------------
# PARAGRAPH CLOZE / BUILDER MODE SERVICES
# -----------------------------------------------------------------------------

def _build_paragraph(blueprint: ParagraphBlueprint, paragraph_number: int, rng: random.Random) -> dict[str, Any]:
    blanks_data: list[dict[str, Any]] = []
    for blank in blueprint.blanks:
        options = [blank.correct_answer, *blank.distractors]
        rng.shuffle(options)
        correct_index = options.index(blank.correct_answer)
        correct_letter = LETTERS[correct_index]

        blanks_data.append(
            {
                "blank_id": blank.blank_id,
                "options": _lettered_options(options),
                "correct_answer": correct_letter,
                "correct_answer_text": blank.correct_answer,
                "grammar_topic": blank.topic,
                "secondary_topics": list(blank.secondary_topics),
                "rule": blank.rule,
                "explanation": blank.explanation,
                "selected_answer": None,
                "is_correct": None,
            }
        )

    return {
        "id": f"p{paragraph_number}",
        "paragraph_number": paragraph_number,
        "title": blueprint.title,
        "text_with_blanks": blueprint.text_with_blanks,
        "full_text": blueprint.full_text,
        "paragraph_explanation": blueprint.paragraph_explanation,
        "level": blueprint.level,
        "blanks": blanks_data,
        "completed": False,
    }


def _generated_paragraph_blueprints(count: int = 3, level: str = "all") -> list[ParagraphBlueprint]:
    _ensure_seeded_bank()
    normalized_level = normalize_level(level)

    bank_count = (
        ParagraphBankQuestion.objects.filter(level=normalized_level).count()
        if normalized_level != "all"
        else ParagraphBankQuestion.objects.count()
    )

    generate_count = count if bank_count < 100 else 0
    generated: list[ParagraphBlueprint] = []
    if generate_count > 0:
        try:
            generated = generate_paragraph_blueprints(generate_count, level=normalized_level)
        except Exception:
            generated = []

    if generated:
        ParagraphBankQuestion.save_blueprints(
            generated,
            source="openrouter",
            generation_metadata={"bank_size_before": bank_count, "requested_level": normalized_level},
        )
        return generated

    sampled_entries = ParagraphBankQuestion.random_sample(
        count,
        level=normalized_level if normalized_level != "all" else None,
    )
    if not sampled_entries:
        sampled_entries = ParagraphBankQuestion.random_sample(count)
    if not sampled_entries:
        raise ValueError("Not enough paragraphs in the bank.")

    return [entry.to_blueprint() for entry in sampled_entries]


def create_paragraph_test_state(total_paragraphs: int = 3, level: str = "all") -> dict[str, Any]:
    rng = _randomizer()
    normalized_level = normalize_level(level)
    selected_blueprints = _generated_paragraph_blueprints(count=total_paragraphs, level=normalized_level)
    paragraphs = [_build_paragraph(bp, idx + 1, rng) for idx, bp in enumerate(selected_blueprints)]
    total_blanks = sum(len(p["blanks"]) for p in paragraphs)

    return {
        "id": uuid.uuid4().hex,
        "test_type": "paragraph",
        "mode": "paragraph",
        "level": normalized_level,
        "total_paragraphs": len(paragraphs),
        "total_questions": total_blanks,
        "current_index": 0,
        "score": 0,
        "completed": False,
        "questions": paragraphs,
    }


def public_paragraph_payload(paragraph: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": paragraph["id"],
        "paragraph_number": paragraph["paragraph_number"],
        "title": paragraph["title"],
        "text_with_blanks": paragraph["text_with_blanks"],
        "level": paragraph["level"],
        "blanks": [
            {
                "blank_id": b["blank_id"],
                "options": b["options"],
                "selected_answer": b["selected_answer"],
            }
            for b in paragraph["blanks"]
        ],
    }


# -----------------------------------------------------------------------------
# COMMON PAYLOAD & STATE HANDLING
# -----------------------------------------------------------------------------

def current_question_payload(state: dict[str, Any]) -> dict[str, Any] | None:
    test_type = state.get("test_type") or state.get("mode") or "sentence"
    if test_type == "writing":
        total_tasks = state.get("total_tasks", len(state["questions"]))
        if state["current_index"] >= total_tasks:
            return None
        return public_writing_payload(state["questions"][state["current_index"]])

    if test_type == "paragraph":
        if state["current_index"] >= state.get("total_paragraphs", len(state["questions"])):
            return None
        return public_paragraph_payload(state["questions"][state["current_index"]])

    if state["current_index"] >= state["total_questions"]:
        return None
    return public_question_payload(state["questions"][state["current_index"]])


def _selected_choice_display(options: list[dict[str, str]], label: str | None) -> str:
    if not label:
        return "[no answer]"
    option = next((opt for opt in options if opt["label"] == label), None)
    if option is None:
        return f"{label}. [unknown option]"
    return _format_choice(option["label"], option["text"])


def _build_feedback(question: dict[str, Any]) -> dict[str, Any]:
    selected_label = question["selected_answer"]
    correct_label = question["correct_answer"]
    selected_display = _selected_choice_display(question["options"], selected_label)
    correct_display = _selected_choice_display(question["options"], correct_label)
    is_correct = bool(question.get("is_correct"))
    rule = question["rule"]
    correct_reason = question["explanation"]

    if is_correct:
        headline = "Correct!"
        reason_right = correct_reason
        reason_wrong = "-"
        incorrect_reason = "-"
    else:
        headline = "Incorrect."
        reason_right = "-"
        selected_text = selected_display.split(". ", 1)[1] if ". " in selected_display else selected_display
        reason_wrong = f"{selected_text} does not fit because {rule[0].lower() + rule[1:]}"
        incorrect_reason = reason_wrong

    return {
        "headline": headline,
        "is_correct": is_correct,
        "grammar_topic": question["grammar_topic"],
        "level": question.get("level", "intermediate"),
        "correct_answer": correct_display,
        "selected_answer": selected_display,
        "rule": rule,
        "explanation": correct_reason,
        "reason_right": reason_right,
        "reason_wrong": reason_wrong,
        "selected_answer_explanation": incorrect_reason,
        "sentence_explanation": question["sentence_explanation"],
    }


def _build_paragraph_feedback(paragraph: dict[str, Any]) -> dict[str, Any]:
    blanks_feedback = []
    total_correct = 0
    for b in paragraph["blanks"]:
        is_corr = bool(b.get("is_correct"))
        if is_corr:
            total_correct += 1
        sel_display = _selected_choice_display(b["options"], b.get("selected_answer"))
        corr_display = _selected_choice_display(b["options"], b["correct_answer"])
        rule = b["rule"]
        corr_reason = b["explanation"]

        if is_corr:
            reason_right = corr_reason
            reason_wrong = "-"
        else:
            reason_right = "-"
            sel_text = sel_display.split(". ", 1)[1] if ". " in sel_display else sel_display
            reason_wrong = f"{sel_text} does not fit because {rule[0].lower() + rule[1:]}"

        blanks_feedback.append(
            {
                "blank_id": b["blank_id"],
                "is_correct": is_corr,
                "grammar_topic": b["grammar_topic"],
                "correct_answer": corr_display,
                "selected_answer": sel_display,
                "rule": rule,
                "explanation": corr_reason,
                "reason_right": reason_right,
                "reason_wrong": reason_wrong,
            }
        )

    all_correct = total_correct == len(paragraph["blanks"])
    headline = "All blanks correct!" if all_correct else f"{total_correct} of {len(paragraph['blanks'])} blanks correct"

    return {
        "headline": headline,
        "all_correct": all_correct,
        "score_this_paragraph": total_correct,
        "total_blanks_this_paragraph": len(paragraph["blanks"]),
        "level": paragraph.get("level", "intermediate"),
        "title": paragraph["title"],
        "full_text": paragraph["full_text"],
        "paragraph_explanation": paragraph["paragraph_explanation"],
        "blanks_feedback": blanks_feedback,
    }


def submit_answer(state: dict[str, Any], answer_payload: Any) -> dict[str, Any]:
    if state["completed"]:
        raise ValueError("This test has already been completed.")

    test_type = state.get("test_type") or state.get("mode") or "sentence"

    # WRITING MODE SUBMISSION
    if test_type == "writing":
        total_tasks = state.get("total_tasks", len(state["questions"]))
        if state["current_index"] >= total_tasks:
            raise ValueError("No active writing task is available.")

        task = state["questions"][state["current_index"]]
        if task.get("completed"):
            raise ValueError("This writing task has already been submitted.")
        if not isinstance(answer_payload, str):
            raise ValueError("A writing submission must be sent as text.")

        essay = answer_payload.strip()
        if len(essay) > WRITING_MAX_CHARS:
            raise ValueError(
                f"The response is too long. Keep it under {WRITING_MAX_CHARS} characters."
            )
        if len(nlp.WORD_RE.findall(essay)) < WRITING_MIN_SUBMIT_WORDS:
            raise ValueError(
                f"Write at least {WRITING_MIN_SUBMIT_WORDS} words before submitting."
            )

        task["submission"] = _evaluate_essay(task, essay)
        task["completed"] = True
        feedback = _build_writing_feedback(task)

        state["current_index"] += 1
        state["completed"] = state["current_index"] >= total_tasks

        return {
            "feedback": feedback,
            "score": state["score"],
            "completed": state["completed"],
            "progress": {
                "current": min(state["current_index"], total_tasks),
                "total": total_tasks,
            },
            "next_question": None if state["completed"] else current_question_payload(state),
        }

    # PARAGRAPH MODE ANSWER SUBMISSION
    if test_type == "paragraph":
        total_p = state.get("total_paragraphs", len(state["questions"]))
        if state["current_index"] >= total_p:
            raise ValueError("No active paragraph is available.")

        paragraph = state["questions"][state["current_index"]]
        if paragraph.get("completed"):
            raise ValueError("This paragraph has already been answered.")

        # answer_payload should be a dict mapping blank_id string to selected letter: {"1": "A", "2": "C", ...}
        if not isinstance(answer_payload, dict):
            raise ValueError("Paragraph submission must provide answers as a dictionary of blank IDs to chosen letters.")

        for b in paragraph["blanks"]:
            b_id_str = str(b["blank_id"])
            selected_letter = str(answer_payload.get(b_id_str, "")).strip().upper()
            if selected_letter not in LETTERS:
                raise ValueError(f"Answer for Blank [{b['blank_id']}] must be one of A, B, C, D, or E.")
            b["selected_answer"] = selected_letter
            b["is_correct"] = selected_letter == b["correct_answer"]
            if b["is_correct"]:
                state["score"] += 1

        paragraph["completed"] = True
        feedback = _build_paragraph_feedback(paragraph)

        state["current_index"] += 1
        state["completed"] = state["current_index"] >= total_p

        next_question = None
        if not state["completed"]:
            next_question = current_question_payload(state)

        return {
            "feedback": feedback,
            "score": state["score"],
            "completed": state["completed"],
            "progress": {
                "current": min(state["current_index"], total_p),
                "total": total_p,
            },
            "next_question": next_question,
        }

    # SENTENCE MODE ANSWER SUBMISSION
    if state["current_index"] >= state["total_questions"]:
        raise ValueError("No active question is available.")

    selected_label = str(answer_payload).strip().upper() if isinstance(answer_payload, str) else ""
    if selected_label not in LETTERS:
        raise ValueError("Selected answer must be one of A, B, C, D, or E.")

    question = state["questions"][state["current_index"]]
    if question["selected_answer"] is not None:
        raise ValueError("This question has already been answered.")

    question["selected_answer"] = selected_label
    question["is_correct"] = selected_label == question["correct_answer"]
    if question["is_correct"]:
        state["score"] += 1

    feedback = _build_feedback(question)

    state["current_index"] += 1
    state["completed"] = state["current_index"] >= state["total_questions"]

    next_question = None
    if not state["completed"]:
        next_question = current_question_payload(state)

    return {
        "feedback": feedback,
        "score": state["score"],
        "completed": state["completed"],
        "progress": {
            "current": min(state["current_index"], state["total_questions"]),
            "total": state["total_questions"],
        },
        "next_question": next_question,
    }


def _topic_summary(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: dict[str, dict[str, Any]] = {}

    for item in items:
        topic = item["grammar_topic"]
        entry = summary.setdefault(
            topic,
            {"topic": topic, "asked": 0, "correct": 0, "incorrect": 0},
        )
        entry["asked"] += 1
        if item["is_correct"]:
            entry["correct"] += 1
        else:
            entry["incorrect"] += 1

    ordered = sorted(summary.values(), key=lambda i: (-i["asked"], i["topic"]))
    for entry in ordered:
        entry["accuracy"] = round((entry["correct"] / entry["asked"]) * 100) if entry["asked"] else 0

    return ordered


def _question_result_payload(question: dict[str, Any]) -> dict[str, Any]:
    selected = question["selected_answer"]
    selected_display = _selected_choice_display(question["options"], selected) if selected else None
    correct_display = _selected_choice_display(question["options"], question["correct_answer"])
    is_corr = bool(question.get("is_correct"))
    rule = question["rule"]
    corr_reason = question["explanation"]

    if is_corr:
        reason_right = corr_reason
        reason_wrong = "-"
    else:
        reason_right = "-"
        if selected_display:
            sel_text = selected_display.split(". ", 1)[1] if ". " in selected_display else selected_display
        else:
            sel_text = "No answer"
        reason_wrong = f"{sel_text} does not fit because {rule[0].lower() + rule[1:]}"

    return {
        "id": question["id"],
        "question_number": question["question_number"],
        "question": question["question"],
        "options": question["options"],
        "grammar_topic": question["grammar_topic"],
        "grammar_topics": question["grammar_topics"],
        "level": question.get("level", "intermediate"),
        "rule": rule,
        "explanation": corr_reason,
        "reason_right": reason_right,
        "reason_wrong": reason_wrong,
        "sentence_explanation": question["sentence_explanation"],
        "correct_answer": correct_display,
        "selected_answer": selected_display,
        "is_correct": is_corr,
    }


def _paragraph_result_payload(paragraph: dict[str, Any]) -> dict[str, Any]:
    blanks_result = []
    for b in paragraph["blanks"]:
        selected = b.get("selected_answer")
        selected_display = _selected_choice_display(b["options"], selected) if selected else None
        correct_display = _selected_choice_display(b["options"], b["correct_answer"])
        is_corr = bool(b.get("is_correct"))
        rule = b["rule"]
        corr_reason = b["explanation"]

        if is_corr:
            reason_right = corr_reason
            reason_wrong = "-"
        else:
            reason_right = "-"
            if selected_display:
                sel_text = selected_display.split(". ", 1)[1] if ". " in selected_display else selected_display
            else:
                sel_text = "No answer"
            reason_wrong = f"{sel_text} does not fit because {rule[0].lower() + rule[1:]}"

        blanks_result.append(
            {
                "blank_id": b["blank_id"],
                "options": b["options"],
                "grammar_topic": b["grammar_topic"],
                "rule": rule,
                "explanation": corr_reason,
                "reason_right": reason_right,
                "reason_wrong": reason_wrong,
                "correct_answer": correct_display,
                "selected_answer": selected_display,
                "is_correct": is_corr,
            }
        )

    return {
        "id": paragraph["id"],
        "paragraph_number": paragraph["paragraph_number"],
        "title": paragraph["title"],
        "text_with_blanks": paragraph["text_with_blanks"],
        "full_text": paragraph["full_text"],
        "paragraph_explanation": paragraph["paragraph_explanation"],
        "level": paragraph.get("level", "intermediate"),
        "blanks": blanks_result,
    }


def build_results(state: dict[str, Any]) -> dict[str, Any]:
    test_type = state.get("test_type") or state.get("mode") or "sentence"

    if test_type == "writing":
        tasks = state["questions"]
        reports = [_writing_report_payload(task) for task in tasks]
        submitted = [report for report in reports if report.get("bands")]

        if submitted:
            averaged = {
                key: round(sum(report["bands"][key] for report in submitted) / len(submitted) * 2) / 2
                for key in nlp.CRITERIA
            }
        else:
            averaged = {key: 0.0 for key in nlp.CRITERIA}
        overall = nlp.overall_band(averaged) if submitted else 0.0

        return {
            "test_id": state["id"],
            "test_type": "writing",
            "mode": "writing",
            "level": state.get("level", "all"),
            "total_questions": len(tasks),
            "total_tasks": len(tasks),
            "correct_answers": 0,
            "incorrect_answers": 0,
            "overall_band": overall,
            "percentage": round(overall / 9 * 100),
            "criteria_summary": [
                {"key": key, "label": nlp.CRITERION_LABELS[key], "band": averaged[key]}
                for key in nlp.CRITERIA
            ],
            "topic_summary": [],
            "tasks": reports,
            "questions": reports,
        }

    if test_type == "paragraph":
        paragraphs = state["questions"]
        all_blanks: list[dict[str, Any]] = []
        for p in paragraphs:
            all_blanks.extend(p["blanks"])

        total_blanks = len(all_blanks)
        correct_answers = sum(1 for b in all_blanks if b.get("is_correct"))
        incorrect_answers = total_blanks - correct_answers
        percentage = round((correct_answers / total_blanks) * 100) if total_blanks else 0

        return {
            "test_id": state["id"],
            "test_type": "paragraph",
            "mode": "paragraph",
            "level": state.get("level", "all"),
            "total_questions": total_blanks,
            "total_paragraphs": len(paragraphs),
            "correct_answers": correct_answers,
            "incorrect_answers": incorrect_answers,
            "percentage": percentage,
            "topic_summary": _topic_summary(all_blanks),
            "paragraphs": [_paragraph_result_payload(p) for p in paragraphs],
            "questions": [_paragraph_result_payload(p) for p in paragraphs],
        }

    # Sentence mode results
    questions = state["questions"]
    correct_answers = sum(1 for question in questions if question.get("is_correct"))
    total = state["total_questions"]
    incorrect_answers = total - correct_answers
    percentage = round((correct_answers / total) * 100) if total else 0

    return {
        "test_id": state["id"],
        "test_type": "sentence",
        "mode": "sentence",
        "level": state.get("level", "all"),
        "total_questions": total,
        "correct_answers": correct_answers,
        "incorrect_answers": incorrect_answers,
        "percentage": percentage,
        "topic_summary": _topic_summary(questions),
        "questions": [_question_result_payload(question) for question in questions],
    }


def initialise_session_state(level: str = "all", mode: str = "sentence") -> dict[str, Any]:
    normalized_mode = normalize_mode(mode)
    if normalized_mode == "writing":
        return create_writing_test_state(level=level)
    if normalized_mode == "paragraph":
        return create_paragraph_test_state(level=level)
    return create_test_state(level=level)


def save_state(request, state: dict[str, Any]) -> None:
    TestSession.create_from_state(state)
    request.session[TEST_SESSION_KEY] = state["id"]
    request.session.modified = True


def load_state(request) -> dict[str, Any] | None:
    test_id = request.session.get(TEST_SESSION_KEY)
    if not test_id:
        return None

    session = TestSession.load_by_id(test_id)
    if not session:
        return None
    return session.to_state()


# -----------------------------------------------------------------------------
# WRITING MODE SERVICES
# -----------------------------------------------------------------------------
#
# The learner answers a writing task, `practice.nlp` measures the response
# locally, and the language model is asked only for the judgement that cannot
# be computed. Without an API key the local assessment stands on its own.

WRITING_MIN_SUBMIT_WORDS = int(os.environ.get("WRITING_MIN_SUBMIT_WORDS", "25"))
WRITING_AI_MIN_WORDS = int(os.environ.get("WRITING_AI_MIN_WORDS", "40"))
WRITING_MAX_CHARS = int(os.environ.get("WRITING_MAX_CHARS", "20000"))


def _writing_ai_enabled() -> bool:
    if os.environ.get("WRITING_AI_ENABLED", "").strip().lower() in {"0", "false", "no", "off"}:
        return False
    return bool(os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY"))


def _build_writing_task(blueprint: WritingPromptBlueprint, task_number: int) -> dict[str, Any]:
    return {
        "id": f"w{task_number}",
        "task_number": task_number,
        "title": blueprint.title,
        "task_type": blueprint.task_type,
        "prompt": blueprint.prompt,
        "level": blueprint.level,
        "min_words": blueprint.min_words,
        "suggested_minutes": blueprint.suggested_minutes,
        "guidance": list(blueprint.guidance),
        "useful_vocabulary": list(blueprint.useful_vocabulary),
        "model_outline": blueprint.model_outline,
        "submission": None,
        "completed": False,
    }


def _writing_blueprints(count: int, level: str = "all") -> list[WritingPromptBlueprint]:
    """Draw tasks from the seeded bank.

    Writing prompts are deliberately never generated by the model: a fixed bank
    costs nothing and the token budget belongs to the assessment.
    """

    _ensure_seeded_bank()
    normalized_level = normalize_level(level)

    sampled = WritingPromptBankQuestion.random_sample(
        count,
        level=normalized_level if normalized_level != "all" else None,
    )
    if not sampled:
        sampled = WritingPromptBankQuestion.random_sample(count)
    if not sampled:
        raise ValueError("No writing prompts are available in the bank.")

    return [entry.to_blueprint() for entry in sampled]


def create_writing_test_state(total_tasks: int = 1, level: str = "all") -> dict[str, Any]:
    normalized_level = normalize_level(level)
    blueprints = _writing_blueprints(total_tasks, level=normalized_level)
    tasks = [_build_writing_task(blueprint, index + 1) for index, blueprint in enumerate(blueprints)]

    return {
        "id": uuid.uuid4().hex,
        "test_type": "writing",
        "mode": "writing",
        "level": normalized_level,
        "total_tasks": len(tasks),
        "total_questions": len(tasks),
        "current_index": 0,
        "score": 0,
        "completed": False,
        "questions": tasks,
    }


def public_writing_payload(task: dict[str, Any]) -> dict[str, Any]:
    """The task as the learner sees it: no target lexis, no model outline."""

    return {
        "id": task["id"],
        "task_number": task["task_number"],
        "title": task["title"],
        "task_type": task["task_type"],
        "prompt": task["prompt"],
        "level": task["level"],
        "min_words": task["min_words"],
        "suggested_minutes": task["suggested_minutes"],
        "guidance": list(task["guidance"]),
    }


def _percent(value: float) -> int:
    return int(round(value * 100))


def _local_criterion_comments(metrics: dict[str, Any]) -> dict[str, str]:
    """Criterion comments derived only from the measurements."""

    groups = metrics["linker_groups_used"]
    comments = {
        "task_response": (
            f"{metrics['word_count']} words against a {metrics['min_words']}-word minimum, "
            f"developed over {metrics['paragraph_count']} paragraph(s)."
        ),
        "coherence_cohesion": (
            f"{metrics['paragraph_count']} paragraph(s) using cohesive devices from "
            f"{len(groups)} function group(s)"
            + (f" ({', '.join(groups)})." if groups else ".")
        ),
        "lexical_resource": (
            f"{metrics['unique_words']} different words in {metrics['word_count']}; "
            f"{_percent(metrics['beyond_core_ratio'])}% sit outside the most frequent core of English, "
            f"including {len(metrics['academic_words_used'])} academic item(s)."
        ),
        "grammatical_range": (
            f"Sentences average {metrics['average_sentence_length']} words "
            f"(variation {metrics['sentence_length_sd']}); "
            f"{_percent(metrics['complex_sentence_ratio'])}% carry a subordinate clause."
        ),
    }

    if not metrics["meets_min_words"]:
        comments["task_response"] += f" {metrics['words_missing']} more words are needed."
    if metrics["overused_words"]:
        top = metrics["overused_words"][0]
        comments["lexical_resource"] += f" {top['word'].capitalize()} is repeated {top['count']} times."
    if metrics["mechanics_issues"]:
        comments["grammatical_range"] += f" {len(metrics['mechanics_issues'])} mechanical issue(s) found."

    return comments


def _local_strengths(metrics: dict[str, Any]) -> list[str]:
    strengths: list[str] = []

    if metrics["beyond_core_ratio"] >= 0.40:
        strengths.append(
            f"Vocabulary reaches well beyond everyday English: {_percent(metrics['beyond_core_ratio'])}% "
            "of your words fall outside the most frequent core."
        )
    if len(metrics["academic_words_used"]) >= 4:
        sample = ", ".join(metrics["academic_words_used"][:4])
        strengths.append(f"You use precise academic vocabulary such as {sample}.")
    if len(metrics["linker_groups_used"]) >= 4:
        strengths.append(
            "Cohesion is handled with a wide range of devices covering "
            f"{', '.join(metrics['linker_groups_used'])}."
        )
    if metrics["complex_sentence_ratio"] >= 0.40:
        strengths.append(
            f"{_percent(metrics['complex_sentence_ratio'])}% of your sentences contain a subordinate clause, "
            "which demonstrates grammatical range."
        )
    if metrics["sentence_length_sd"] >= 5:
        strengths.append(
            f"Sentence length varies (average {metrics['average_sentence_length']} words, "
            f"spread {metrics['sentence_length_sd']}), so the writing does not read mechanically."
        )
    if metrics["paragraph_count"] >= 3 and min(metrics["paragraph_sentence_counts"] or [0]) >= 2:
        strengths.append(
            f"The response is organised into {metrics['paragraph_count']} developed paragraphs."
        )
    if metrics["meets_min_words"]:
        strengths.append(f"The response meets the {metrics['min_words']}-word requirement.")
    if not metrics["mechanics_issues"]:
        strengths.append("Capitalisation, spacing, and punctuation are clean throughout.")

    return strengths[:5]


def _local_improvements(metrics: dict[str, Any]) -> list[str]:
    improvements: list[str] = []

    if not metrics["meets_min_words"]:
        improvements.append(
            f"Add roughly {metrics['words_missing']} more words to reach the "
            f"{metrics['min_words']}-word minimum."
        )

    for item in metrics["overused_words"][:2]:
        alternatives = nlp.BASIC_UPGRADES.get(item["word"])
        suggestion = (
            f" Try {', '.join(alternatives[:3])}."
            if alternatives
            else " Refer back to it with a synonym, a pronoun, or a related noun phrase."
        )
        improvements.append(
            f"You repeat \"{item['word']}\" {item['count']} times.{suggestion}"
        )

    if metrics["paragraph_count"] < 3:
        improvements.append(
            "Organise the answer into at least three paragraphs - an introduction, developed body "
            "paragraphs, and a conclusion - each opening with a topic sentence."
        )

    missing_groups = [group for group in ("contrast", "cause", "example", "conclusion") if group not in metrics["linker_groups_used"]]
    if len(metrics["linker_groups_used"]) <= 2 and missing_groups:
        improvements.append(
            "Widen your cohesive devices: you have no "
            f"{', '.join(missing_groups)} linkers (for example however, therefore, for instance, on balance)."
        )

    if metrics["complex_sentence_ratio"] < 0.25:
        improvements.append(
            "Most of your sentences are simple. Combine ideas with although, whereas, which, or since "
            "to show a wider range of structures."
        )
    elif metrics["sentence_length_sd"] < 3 and metrics["sentence_count"] >= 4:
        improvements.append(
            "Sentence length barely varies. Follow a long developed sentence with a short emphatic one."
        )

    if not metrics["has_conclusion_signal"] and metrics["word_count"] >= 60:
        improvements.append(
            "Close with an explicit conclusion signalled by In conclusion, Overall, or On balance."
        )

    if metrics["repeated_openers"]:
        opener = metrics["repeated_openers"][0]
        improvements.append(
            f"{opener['count']} sentences begin with \"{opener['opener']}\". Vary your sentence openings "
            "with an adverbial or a subordinate clause."
        )

    if metrics["informal_expressions"]:
        improvements.append(
            "Replace conversational expressions ("
            + ", ".join(metrics["informal_expressions"][:3])
            + ") with formal equivalents."
        )
    elif metrics["contraction_count"] >= 3:
        improvements.append(
            f"You use {metrics['contraction_count']} contractions. Write them in full in formal writing."
        )

    if metrics["mechanics_issues"]:
        improvements.append("Fix the mechanics: " + "; ".join(metrics["mechanics_issues"][:2]) + ".")

    if metrics["average_sentence_length"] > 30:
        improvements.append(
            f"Sentences average {metrics['average_sentence_length']} words. Split the longest ones so each "
            "carries a single idea."
        )

    return improvements[:6]


_DEDUP_IGNORE = frozenset(
    {
        "with", "your", "that", "this", "each", "more", "than", "into", "from", "them",
        "they", "when", "will", "would", "have", "been", "their", "there", "where",
        "which", "should", "could", "rather", "instead", "response", "answer", "writing",
    }
)


def _restates(candidate: str, existing: list[str]) -> bool:
    """True when `candidate` makes substantially the same point as an existing item."""

    def keywords(text: str) -> set[str]:
        return {
            word
            for word in re.findall(r"[a-z]+", text.lower())
            if len(word) > 3 and word not in _DEDUP_IGNORE
        }

    candidate_keys = keywords(candidate)
    if not candidate_keys:
        return False

    for item in existing:
        item_keys = keywords(item)
        if not item_keys:
            continue
        shared = len(candidate_keys & item_keys)
        if max(shared / len(candidate_keys), shared / len(item_keys)) >= 0.5:
            return True
    return False


def _merge_vocabulary_upgrades(
    ai_upgrades: list[dict[str, str]],
    metrics: dict[str, Any],
) -> list[dict[str, str]]:
    """Examiner suggestions first, then measured ones that add something new."""

    merged: list[dict[str, str]] = []
    seen: set[str] = set()

    for item in ai_upgrades:
        key = item["basic"].lower()
        if key in seen:
            continue
        seen.add(key)
        merged.append({"basic": item["basic"], "stronger": item["stronger"], "source": "examiner"})

    for item in metrics["basic_word_upgrades"]:
        key = item["basic"].lower()
        if key in seen:
            continue
        seen.add(key)
        merged.append(
            {
                "basic": item["basic"],
                "stronger": ", ".join(item["suggestions"]),
                "source": "measured",
                "count": item["count"],
            }
        )

    return merged[:10]


def _evaluate_essay(task: dict[str, Any], essay: str) -> dict[str, Any]:
    """Measure locally, then spend tokens on judgement only."""

    metrics = nlp.analyze_writing(essay, min_words=task["min_words"])
    local_bands = metrics["local_bands"]

    ai_report: dict[str, Any] | None = None
    ai_error: str | None = None
    if _writing_ai_enabled() and metrics["word_count"] >= WRITING_AI_MIN_WORDS:
        try:
            ai_report = evaluate_writing(
                essay=essay,
                digest=metrics["digest"],
                local_bands=local_bands,
                task_title=task["title"],
                task_prompt=task["prompt"],
                level=task["level"],
            )
        except Exception as exc:  # any failure falls back to the local assessment
            ai_error = f"{type(exc).__name__}: {exc}"[:200]

    assessed_by = "examiner" if ai_report else "measured"
    bands = dict(ai_report["bands"]) if ai_report else dict(local_bands)
    bands, notes = nlp.apply_length_penalty(bands, metrics)

    comments = ai_report["comments"] if ai_report else _local_criterion_comments(metrics)
    criteria = [
        {
            "key": key,
            "label": nlp.CRITERION_LABELS[key],
            "band": bands[key],
            "comment": comments.get(key, ""),
            "measured_band": local_bands[key],
        }
        for key in nlp.CRITERIA
    ]

    local_improvements = _local_improvements(metrics)
    if ai_report:
        strengths = ai_report["strengths"] or _local_strengths(metrics)
        improvements = ai_report["improvements"] or local_improvements
        # Keep only the measured points the examiner did not already make.
        measured_observations = [
            observation
            for observation in local_improvements
            if not _restates(observation, improvements)
        ]
    else:
        strengths = _local_strengths(metrics)
        improvements = local_improvements
        measured_observations = []
        if metrics["word_count"] < WRITING_AI_MIN_WORDS:
            notes.append(
                f"Responses under {WRITING_AI_MIN_WORDS} words are scored locally only, without an examiner review."
            )
        elif not _writing_ai_enabled():
            notes.append(
                "No model is configured, so these bands come from the local analysis alone. It measures "
                "length, vocabulary range, structure, and cohesion, but it cannot judge how well your "
                "ideas answer the question."
            )
        elif ai_error:
            notes.append("The examiner review could not be reached, so the local analysis was used instead.")

    return {
        "essay": essay,
        "metrics": metrics,
        "bands": bands,
        "measured_bands": local_bands,
        "overall_band": nlp.overall_band(bands),
        "measured_overall_band": nlp.overall_band(local_bands),
        "criteria": criteria,
        "strengths": strengths,
        "improvements": improvements,
        "measured_observations": measured_observations,
        "corrections": ai_report["corrections"] if ai_report else [],
        "vocabulary_upgrades": _merge_vocabulary_upgrades(
            ai_report["vocabulary_upgrades"] if ai_report else [],
            metrics,
        ),
        "notes": notes,
        "assessed_by": assessed_by,
        "ai_error": ai_error,
        "model": ai_report.get("model") if ai_report else None,
        "usage": ai_report.get("usage") if ai_report else None,
        "revealed": {
            "useful_vocabulary": list(task["useful_vocabulary"]),
            "model_outline": task["model_outline"],
        },
    }


def _writing_report_payload(task: dict[str, Any]) -> dict[str, Any]:
    submission = task.get("submission") or {}
    return {
        "id": task["id"],
        "task_number": task["task_number"],
        "title": task["title"],
        "task_type": task["task_type"],
        "prompt": task["prompt"],
        "level": task["level"],
        "min_words": task["min_words"],
        "suggested_minutes": task["suggested_minutes"],
        "guidance": list(task["guidance"]),
        **submission,
    }


def _build_writing_feedback(task: dict[str, Any]) -> dict[str, Any]:
    submission = task.get("submission") or {}
    band = submission.get("overall_band", 0.0)
    return {
        "headline": f"Estimated IELTS band {band:.1f}",
        **_writing_report_payload(task),
    }
