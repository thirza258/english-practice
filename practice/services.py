from __future__ import annotations

import random
import uuid
from typing import Any

from .ai import generate_paragraph_blueprints, generate_question_blueprints
from .models import ParagraphBankQuestion, QuestionBankQuestion, TestSession
from .question_bank import ParagraphBlueprint, QuestionBlueprint


LETTERS = ["A", "B", "C", "D", "E"]
TEST_SESSION_KEY = "english_practice_active_test"
SUPPORTED_LEVELS = ("all", "beginner", "intermediate", "advanced", "ielts_8_9")
SUPPORTED_MODES = ("sentence", "paragraph")


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
    is_correct = question["is_correct"]
    rule = question["rule"]
    correct_reason = question["explanation"]

    if is_correct:
        incorrect_reason = "Your selection matches the grammar rule."
        headline = "Correct!"
    else:
        selected_text = selected_display.split(". ", 1)[1] if ". " in selected_display else selected_display
        incorrect_reason = f"{selected_text} does not fit because {rule[0].lower() + rule[1:]}"
        headline = "Incorrect."

    return {
        "headline": headline,
        "is_correct": is_correct,
        "grammar_topic": question["grammar_topic"],
        "level": question.get("level", "intermediate"),
        "correct_answer": correct_display,
        "selected_answer": selected_display,
        "rule": rule,
        "explanation": correct_reason,
        "selected_answer_explanation": incorrect_reason,
        "sentence_explanation": question["sentence_explanation"],
    }


def _build_paragraph_feedback(paragraph: dict[str, Any]) -> dict[str, Any]:
    blanks_feedback = []
    total_correct = 0
    for b in paragraph["blanks"]:
        is_corr = b["is_correct"]
        if is_corr:
            total_correct += 1
        sel_display = _selected_choice_display(b["options"], b["selected_answer"])
        corr_display = _selected_choice_display(b["options"], b["correct_answer"])

        blanks_feedback.append(
            {
                "blank_id": b["blank_id"],
                "is_correct": is_corr,
                "grammar_topic": b["grammar_topic"],
                "correct_answer": corr_display,
                "selected_answer": sel_display,
                "rule": b["rule"],
                "explanation": b["explanation"],
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

    return {
        "id": question["id"],
        "question_number": question["question_number"],
        "question": question["question"],
        "options": question["options"],
        "grammar_topic": question["grammar_topic"],
        "grammar_topics": question["grammar_topics"],
        "level": question.get("level", "intermediate"),
        "rule": question["rule"],
        "explanation": question["explanation"],
        "sentence_explanation": question["sentence_explanation"],
        "correct_answer": correct_display,
        "selected_answer": selected_display,
        "is_correct": question["is_correct"],
    }


def _paragraph_result_payload(paragraph: dict[str, Any]) -> dict[str, Any]:
    blanks_result = []
    for b in paragraph["blanks"]:
        selected = b["selected_answer"]
        selected_display = _selected_choice_display(b["options"], selected) if selected else None
        correct_display = _selected_choice_display(b["options"], b["correct_answer"])

        blanks_result.append(
            {
                "blank_id": b["blank_id"],
                "options": b["options"],
                "grammar_topic": b["grammar_topic"],
                "rule": b["rule"],
                "explanation": b["explanation"],
                "correct_answer": correct_display,
                "selected_answer": selected_display,
                "is_correct": b["is_correct"],
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
