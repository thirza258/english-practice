from __future__ import annotations

import random
import uuid
from typing import Any

from .ai import generate_question_blueprints
from .models import QuestionBankQuestion, TestSession
from .question_bank import QuestionBlueprint


LETTERS = ["A", "B", "C", "D", "E"]
TEST_SESSION_KEY = "english_practice_active_test"


def _randomizer() -> random.Random:
    return random.SystemRandom()


def _ensure_seeded_bank() -> None:
    QuestionBankQuestion.seed_from_static_bank()


def _lettered_options(options: list[str]) -> list[dict[str, str]]:
    return [{"label": label, "text": text} for label, text in zip(LETTERS, options, strict=True)]


def _format_choice(label: str, text: str) -> str:
    return f"{label}. {text}"


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
        "rule": blueprint.rule,
        "explanation": blueprint.explanation,
        "sentence_explanation": blueprint.sentence_explanation,
        "selected_answer": None,
        "is_correct": None,
    }


def _generated_blueprints(total_questions: int) -> list[QuestionBlueprint]:
    _ensure_seeded_bank()

    bank_count = QuestionBankQuestion.objects.count()
    generate_count = total_questions if bank_count < 500 else min(5, total_questions)

    generated: list[QuestionBlueprint] = []
    if generate_count > 0:
        try:
            generated = generate_question_blueprints(generate_count)
        except Exception:
            generated = []

    if generated:
        QuestionBankQuestion.save_blueprints(
            generated,
            source="openrouter",
            generation_metadata={"bank_size_before": bank_count},
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
            )
            for blueprint in generated
        }
        sampled_entries = QuestionBankQuestion.random_sample(
            sampled_count,
            exclude_hashes=exclude_hashes,
        )
        if len(sampled_entries) < sampled_count:
            sampled_entries = QuestionBankQuestion.random_sample(sampled_count)

        combined = [*generated, *(entry.to_blueprint() for entry in sampled_entries)]
        rng = _randomizer()
        rng.shuffle(combined)
        return combined

    if generated:
        return generated

    sampled_entries = QuestionBankQuestion.random_sample(total_questions)
    if len(sampled_entries) < total_questions:
        raise ValueError("Not enough questions in the bank to build a test.")
    return [entry.to_blueprint() for entry in sampled_entries]


def create_test_state(total_questions: int = 10) -> dict[str, Any]:
    rng = _randomizer()
    selected_blueprints = _generated_blueprints(total_questions)
    questions = [_build_question(blueprint, index + 1, rng) for index, blueprint in enumerate(selected_blueprints)]

    return {
        "id": uuid.uuid4().hex,
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


def current_question_payload(state: dict[str, Any]) -> dict[str, Any] | None:
    if state["current_index"] >= state["total_questions"]:
        return None
    return public_question_payload(state["questions"][state["current_index"]])


def _selected_choice_display(question: dict[str, Any], label: str) -> str:
    option = next((option for option in question["options"] if option["label"] == label), None)
    if option is None:
        return f"{label}. [unknown option]"
    return _format_choice(option["label"], option["text"])


def _build_feedback(question: dict[str, Any]) -> dict[str, Any]:
    selected_label = question["selected_answer"]
    correct_label = question["correct_answer"]
    selected_display = _selected_choice_display(question, selected_label)
    correct_display = _selected_choice_display(question, correct_label)
    is_correct = question["is_correct"]
    rule = question["rule"]
    correct_reason = question["explanation"]

    if is_correct:
        incorrect_reason = "Your selection matches the grammar rule."
        headline = "Correct!"
    else:
        selected_text = selected_display.split(". ", 1)[1]
        incorrect_reason = f"{selected_text} does not fit because {rule[0].lower() + rule[1:]}"
        headline = "Incorrect."

    return {
        "headline": headline,
        "is_correct": is_correct,
        "grammar_topic": question["grammar_topic"],
        "correct_answer": correct_display,
        "selected_answer": selected_display,
        "rule": rule,
        "explanation": correct_reason,
        "selected_answer_explanation": incorrect_reason,
        "sentence_explanation": question["sentence_explanation"],
    }


def submit_answer(state: dict[str, Any], selected_label: str) -> dict[str, Any]:
    if state["completed"]:
        raise ValueError("This test has already been completed.")

    if state["current_index"] >= state["total_questions"]:
        raise ValueError("No active question is available.")

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


def _topic_summary(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: dict[str, dict[str, Any]] = {}

    for question in questions:
        topic = question["grammar_topic"]
        entry = summary.setdefault(
            topic,
            {"topic": topic, "asked": 0, "correct": 0, "incorrect": 0},
        )
        entry["asked"] += 1
        if question["is_correct"]:
            entry["correct"] += 1
        else:
            entry["incorrect"] += 1

    ordered = sorted(summary.values(), key=lambda item: (-item["asked"], item["topic"]))
    for entry in ordered:
        entry["accuracy"] = round((entry["correct"] / entry["asked"]) * 100) if entry["asked"] else 0

    return ordered


def _question_result_payload(question: dict[str, Any]) -> dict[str, Any]:
    selected = question["selected_answer"]
    selected_display = _selected_choice_display(question, selected) if selected else None
    correct_display = _selected_choice_display(question, question["correct_answer"])

    return {
        "id": question["id"],
        "question_number": question["question_number"],
        "question": question["question"],
        "options": question["options"],
        "grammar_topic": question["grammar_topic"],
        "grammar_topics": question["grammar_topics"],
        "rule": question["rule"],
        "explanation": question["explanation"],
        "sentence_explanation": question["sentence_explanation"],
        "correct_answer": correct_display,
        "selected_answer": selected_display,
        "is_correct": question["is_correct"],
    }


def build_results(state: dict[str, Any]) -> dict[str, Any]:
    questions = state["questions"]
    correct_answers = sum(1 for question in questions if question["is_correct"])
    total = state["total_questions"]
    incorrect_answers = total - correct_answers
    percentage = round((correct_answers / total) * 100) if total else 0

    return {
        "test_id": state["id"],
        "total_questions": total,
        "correct_answers": correct_answers,
        "incorrect_answers": incorrect_answers,
        "percentage": percentage,
        "topic_summary": _topic_summary(questions),
        "questions": [_question_result_payload(question) for question in questions],
    }


def initialise_session_state() -> dict[str, Any]:
    return create_test_state()


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
