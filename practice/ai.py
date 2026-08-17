from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI

from .question_bank import QUESTION_BANK, QuestionBlueprint


OPENROUTER_BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_APP_TITLE = os.environ.get("OPENROUTER_APP_TITLE", "English Practice Diagnostic")
OPENROUTER_REFERER = os.environ.get("OPENROUTER_REFERER")

SUPPORTED_TOPICS = [question.topic for question in QUESTION_BANK]


def _client() -> OpenAI:
    api_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is required for AI question generation.")

    headers: dict[str, str] = {"X-Title": OPENROUTER_APP_TITLE}
    if OPENROUTER_REFERER:
        headers["HTTP-Referer"] = OPENROUTER_REFERER

    return OpenAI(
        api_key=api_key,
        base_url=OPENROUTER_BASE_URL,
        default_headers=headers,
    )


def _prompt(total_questions: int) -> list[dict[str, str]]:
    topics = "\n".join(f"- {topic}" for topic in SUPPORTED_TOPICS)
    system = (
        "You generate English grammar diagnostic questions for a web app. "
        "Return only valid JSON. Do not use markdown. "
        "Every question must have exactly one correct answer, four plausible distractors, "
        "a hidden grammar topic, a short rule, a concise explanation, and a sentence-based explanation. "
        "The visible question text must not reveal the topic."
    )
    user = f"""
Generate exactly {total_questions} multiple-choice grammar questions.

Rules:
- Use only topics from this list.
- Topics may repeat, but the set should feel varied.
- Each question must have exactly one clearly correct answer.
- Each question must include four distinct distractors.
- The correct answer should be the exact value of "correct_answer".
- Do not include answer letters.
- Do not reveal the topic in the question text.
- Keep questions natural and concise.

Allowed topics:
{topics}

Return JSON in this shape:
{{
  "questions": [
    {{
      "topic": "one of the allowed topics",
      "question": "sentence with one blank",
      "correct_answer": "answer text",
      "distractors": ["wrong 1", "wrong 2", "wrong 3", "wrong 4"],
      "rule": "short grammar rule",
      "explanation": "why the correct answer works",
      "sentence_explanation": "the completed sentence",
      "secondary_topics": ["optional secondary topic"]
    }}
  ]
}}
""".strip()
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def _validate_question(item: dict[str, Any]) -> QuestionBlueprint:
    required_fields = ("topic", "question", "correct_answer", "distractors", "rule", "explanation", "sentence_explanation")
    for field in required_fields:
        if field not in item:
            raise ValueError(f"AI output is missing required field: {field}")

    topic = str(item["topic"]).strip()
    if topic not in SUPPORTED_TOPICS:
        raise ValueError(f"Unsupported topic returned by AI: {topic}")

    question = str(item["question"]).strip()
    if not question:
        raise ValueError("AI output included an empty question.")
    if topic.lower() in question.lower():
        raise ValueError("AI output revealed the topic in the question text.")

    correct_answer = str(item["correct_answer"]).strip()
    distractors = [str(choice).strip() for choice in item["distractors"]]

    if not correct_answer:
        raise ValueError("AI output included an empty correct answer.")
    if len(distractors) != 4:
        raise ValueError("AI output must include exactly four distractors.")
    if len({correct_answer, *distractors}) != 5:
        raise ValueError("AI output must contain five unique answer options.")

    rule = str(item["rule"]).strip()
    explanation = str(item["explanation"]).strip()
    sentence_explanation = str(item["sentence_explanation"]).strip()
    if not rule or not explanation or not sentence_explanation:
        raise ValueError("AI output included an empty explanation field.")

    secondary_topics = tuple(str(value).strip() for value in item.get("secondary_topics", []) if str(value).strip())

    return QuestionBlueprint(
        topic=topic,
        question=question,
        correct_answer=correct_answer,
        distractors=tuple(distractors),
        rule=rule,
        explanation=explanation,
        sentence_explanation=sentence_explanation,
        secondary_topics=secondary_topics,
    )


def generate_question_blueprints(total_questions: int) -> list[QuestionBlueprint]:
    client = _client()
    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=_prompt(total_questions),
        temperature=0.8,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content or "{}"
    data = json.loads(content)
    questions = data.get("questions")
    if not isinstance(questions, list):
        raise ValueError("AI output did not include a questions array.")
    if len(questions) != total_questions:
        raise ValueError(f"AI output must contain exactly {total_questions} questions.")

    blueprints = [_validate_question(item) for item in questions]
    if len({blueprint.question.strip().lower() for blueprint in blueprints}) != total_questions:
        raise ValueError("AI output must contain unique question text.")
    return blueprints
