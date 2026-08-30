from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI

from .question_bank import BlankBlueprint, ParagraphBlueprint, QUESTION_BANK, QuestionBlueprint


OPENROUTER_BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_APP_TITLE = os.environ.get("OPENROUTER_APP_TITLE", "English Practice Diagnostic")
OPENROUTER_REFERER = os.environ.get("OPENROUTER_REFERER")

SUPPORTED_TOPICS = sorted({question.topic for question in QUESTION_BANK})
VALID_LEVELS = ("all", "beginner", "intermediate", "advanced", "ielts_8_9")

LEVEL_GUIDANCE: dict[str, str] = {
    "beginner": (
        "Target Level: Beginner (CEFR A1-A2). "
        "Questions must use straightforward vocabulary, simple sentences, and elementary grammar concepts "
        "(e.g., simple tenses, subject-verb agreement with basic subjects, personal pronouns, basic adjectives/adverbs, "
        "simple compound sentences, basic prepositions)."
    ),
    "intermediate": (
        "Target Level: Intermediate (CEFR B1-B2). "
        "Questions should feature moderate complexity, compound/complex sentences, and intermediate grammar concepts "
        "(e.g., adjective/adverb/noun clauses, gerunds & infinitives, present/past participles, degrees of comparison, "
        "appositives, standard conditionals, and prepositional idioms)."
    ),
    "advanced": (
        "Target Level: Advanced (CEFR C1-C2). "
        "Questions should feature sophisticated syntax, challenging distractors, and advanced grammar concepts "
        "(e.g., subjunctive mood, inverted subject and predicate, causative constructions, elliptical constructions, "
        "parallel structure, inverted conditionals, and nuanced English usage/collocations)."
    ),
    "ielts_8_9": (
        "Target Level: IELTS Band 8.0 - 9.0 (C2 / Rare Lexical Resource & Academic Precision). "
        "Sentences must feature sophisticated, low-frequency, erudite vocabulary (e.g., cogent, obfuscate, salutary, "
        "perspicacious, dichotomy, lacuna, exacerbate, antithetical, notwithstanding, punctilious, inefficacious, "
        "supercilious, recalcitrant) embedded in dense, academic syntax (subject-auxiliary inversion, mandative subjunctive, "
        "parallel correlatives, mixed counterfactual conditionals)."
    ),
    "all": (
        "Target Level: Mixed / All Levels (CEFR A1 to C2 & IELTS Band 8-9). "
        "Generate a well-balanced mixture across all proficiency levels."
    ),
}

PARAGRAPH_LEVEL_GUIDANCE: dict[str, str] = {
    "beginner": (
        "Target Level: Beginner (CEFR A1-A2). "
        "Write clear, cohesive paragraphs (3-4 sentences) on daily topics (routines, hobbies, family, weather, travel). "
        "Include 3 blanks testing basic conjunctions (and, but, because, so), pronoun consistency, simple present/past verbs, "
        "and basic prepositions/adjectives."
    ),
    "intermediate": (
        "Target Level: Intermediate (CEFR B1-B2). "
        "Write engaging, well-structured paragraphs (4-5 sentences) on informative or narrative topics (science, habits, culture, nature). "
        "Include 3 blanks testing discourse markers (however, therefore, in addition, although), relative clauses, participles, "
        "gerunds/infinitives, conditionals, and prepositional idioms."
    ),
    "advanced": (
        "Target Level: Advanced (CEFR C1-C2). "
        "Write high-register, academic/essay paragraphs (4-5 sentences) on complex themes (AI & ethics, architecture, psychology, linguistics, philosophy). "
        "Include 3 blanks testing advanced transitions (while, albeit, nonetheless, subsequently), mandative subjunctive, "
        "inverted syntax, parallel correlative structures, and nuanced collocations."
    ),
    "ielts_8_9": (
        "Target Level: IELTS Band 8.0 - 9.0 (C2 / Rare Vocabulary & Scholarly Discourse). "
        "Write dense, scholarly essay passages featuring rare academic vocabulary and high-register discourse markers "
        "(e.g., notwithstanding the fact that, on no account, were [subject] to, incumbent upon). Include 3 blanks testing rare words, "
        "scholarly collocations, and advanced syntactic inversion."
    ),
    "all": (
        "Target Level: Mixed / All Levels (CEFR A1 to C2 & IELTS 8-9). "
        "Generate a diverse set of cohesive paragraph passages ranging from accessible to advanced register."
    ),
}


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


def _prompt(total_questions: int, level: str = "all") -> list[dict[str, str]]:
    topics = "\n".join(f"- {topic}" for topic in SUPPORTED_TOPICS)
    level_key = level.lower() if level.lower() in LEVEL_GUIDANCE else "all"
    guidance = LEVEL_GUIDANCE[level_key]

    system = (
        "You generate English grammar diagnostic questions for a web app. "
        "Return only valid JSON. Do not use markdown. "
        "Every question must have exactly one correct answer, four plausible distractors, "
        "a hidden grammar topic, an English level (beginner, intermediate, or advanced), "
        "a short rule, a concise explanation, and a sentence-based explanation. "
        "The visible question text must not reveal the topic."
    )
    user = f"""
Generate exactly {total_questions} multiple-choice grammar questions.

Difficulty & Level requirement:
{guidance}

Rules:
- Use only topics from this list.
- Topics may repeat, but the set should feel varied.
- Each question must have exactly one clearly correct answer.
- Each question must include four distinct distractors.
- The correct answer should be the exact value of "correct_answer".
- Do not include answer letters in options or answers.
- Do not reveal the topic in the question text.
- Set "level" for each question to "beginner", "intermediate", or "advanced".
- Keep questions natural, accurate, and concise.

Allowed topics:
{topics}

Return JSON in this shape:
{{
  "questions": [
    {{
      "topic": "one of the allowed topics",
      "level": "beginner | intermediate | advanced",
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


def _validate_question(item: dict[str, Any], default_level: str = "intermediate") -> QuestionBlueprint:
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

    item_level = str(item.get("level", "")).strip().lower()
    if item_level not in ("beginner", "intermediate", "advanced", "ielts_8_9"):
        item_level = default_level if default_level in ("beginner", "intermediate", "advanced", "ielts_8_9") else "intermediate"


    return QuestionBlueprint(
        topic=topic,
        question=question,
        correct_answer=correct_answer,
        distractors=tuple(distractors),
        rule=rule,
        explanation=explanation,
        sentence_explanation=sentence_explanation,
        secondary_topics=secondary_topics,
        level=item_level,
    )


def generate_question_blueprints(total_questions: int, level: str = "all") -> list[QuestionBlueprint]:
    client = _client()
    normalized_level = level.lower() if level.lower() in VALID_LEVELS else "all"
    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=_prompt(total_questions, normalized_level),
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

    default_level = normalized_level if normalized_level in ("beginner", "intermediate", "advanced") else "intermediate"
    blueprints = [_validate_question(item, default_level=default_level) for item in questions]
    if len({blueprint.question.strip().lower() for blueprint in blueprints}) != total_questions:
        raise ValueError("AI output must contain unique question text.")
    return blueprints


# -----------------------------------------------------------------------------
# PARAGRAPH CLOZE / BUILDER AI GENERATION
# -----------------------------------------------------------------------------

def _paragraph_prompt(count: int, level: str = "all") -> list[dict[str, str]]:
    level_key = level.lower() if level.lower() in PARAGRAPH_LEVEL_GUIDANCE else "all"
    guidance = PARAGRAPH_LEVEL_GUIDANCE[level_key]

    system = (
        "You generate English paragraph practice cloze exercises for an interactive web app. "
        "Each exercise presents a coherent, well-written paragraph containing exactly 3 numbered blanks marked as [1], [2], and [3]. "
        "For each blank, provide 1 correct answer and 4 plausible distractors (5 choices total). "
        "Explain the grammar/cohesion rule for each blank, and provide a paragraph-level explanation teaching paragraph cohesion, flow, and structure. "
        "Return only valid JSON without markdown formatting."
    )

    user = f"""
Generate exactly {count} paragraph cloze exercises.

Difficulty & Level Guidance:
{guidance}

Rules:
- Each paragraph must be cohesive, natural English with exactly 3 blanks marked as [1], [2], and [3].
- Each blank must have exactly 1 clearly correct answer and exactly 4 plausible distractors.
- For each blank, specify topic, rule, explanation, and distractors.
- Provide "full_text" (the complete paragraph without blanks) and "paragraph_explanation" (explaining paragraph structure, transitions, and cohesion).
- Set "level" to "beginner", "intermediate", or "advanced".

Return JSON in this shape:
{{
  "paragraphs": [
    {{
      "title": "Topic title",
      "level": "beginner | intermediate | advanced",
      "text_with_blanks": "Paragraph text with [1], [2], and [3] markers...",
      "full_text": "Completed paragraph text...",
      "paragraph_explanation": "Paragraph Building: explanation of cohesion, structure, and transitions...",
      "blanks": [
        {{
          "blank_id": 1,
          "topic": "grammar or discourse topic",
          "correct_answer": "correct word/phrase",
          "distractors": ["wrong 1", "wrong 2", "wrong 3", "wrong 4"],
          "rule": "grammar or writing rule",
          "explanation": "why this choice fits into the paragraph context"
        }},
        {{
          "blank_id": 2,
          "topic": "...",
          "correct_answer": "...",
          "distractors": ["...", "...", "...", "..."],
          "rule": "...",
          "explanation": "..."
        }},
        {{
          "blank_id": 3,
          "topic": "...",
          "correct_answer": "...",
          "distractors": ["...", "...", "...", "..."],
          "rule": "...",
          "explanation": "..."
        }}
      ]
    }}
  ]
}}
""".strip()
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def _validate_paragraph(item: dict[str, Any], default_level: str = "intermediate") -> ParagraphBlueprint:
    required_fields = ("title", "text_with_blanks", "full_text", "paragraph_explanation", "blanks")
    for field in required_fields:
        if field not in item:
            raise ValueError(f"AI paragraph output is missing required field: {field}")

    title = str(item["title"]).strip() or "Paragraph Exercise"
    text_with_blanks = str(item["text_with_blanks"]).strip()
    full_text = str(item["full_text"]).strip()
    paragraph_explanation = str(item["paragraph_explanation"]).strip()

    if not text_with_blanks or not full_text or not paragraph_explanation:
        raise ValueError("AI paragraph output contained empty text or explanation.")

    blanks_data = item.get("blanks")
    if not isinstance(blanks_data, list) or len(blanks_data) < 2:
        raise ValueError("AI paragraph output must contain at least 2 blanks.")

    blanks: list[BlankBlueprint] = []
    for idx, b in enumerate(blanks_data, start=1):
        topic = str(b.get("topic", "Paragraph Grammar")).strip()
        correct_answer = str(b.get("correct_answer", "")).strip()
        distractors = [str(d).strip() for d in b.get("distractors", [])]
        rule = str(b.get("rule", "")).strip()
        explanation = str(b.get("explanation", "")).strip()

        if not correct_answer:
            raise ValueError(f"Blank {idx} is missing a correct answer.")
        if len(distractors) != 4:
            raise ValueError(f"Blank {idx} must have exactly 4 distractors.")
        if len({correct_answer, *distractors}) != 5:
            raise ValueError(f"Blank {idx} must have 5 unique choices.")
        if not rule or not explanation:
            raise ValueError(f"Blank {idx} is missing rule or explanation.")

        blanks.append(
            BlankBlueprint(
                blank_id=b.get("blank_id", idx),
                topic=topic,
                correct_answer=correct_answer,
                distractors=tuple(distractors),
                rule=rule,
                explanation=explanation,
                secondary_topics=tuple(str(s).strip() for s in b.get("secondary_topics", []) if str(s).strip()),
            )
        )

    item_level = str(item.get("level", "")).strip().lower()
    if item_level not in ("beginner", "intermediate", "advanced", "ielts_8_9"):
        item_level = default_level if default_level in ("beginner", "intermediate", "advanced", "ielts_8_9") else "intermediate"


    return ParagraphBlueprint(
        title=title,
        text_with_blanks=text_with_blanks,
        blanks=tuple(blanks),
        level=item_level,
        full_text=full_text,
        paragraph_explanation=paragraph_explanation,
    )


def generate_paragraph_blueprints(count: int, level: str = "all") -> list[ParagraphBlueprint]:
    client = _client()
    normalized_level = level.lower() if level.lower() in VALID_LEVELS else "all"
    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=_paragraph_prompt(count, normalized_level),
        temperature=0.8,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content or "{}"
    data = json.loads(content)
    paragraphs = data.get("paragraphs")
    if not isinstance(paragraphs, list):
        raise ValueError("AI output did not include a paragraphs array.")
    if len(paragraphs) != count:
        raise ValueError(f"AI output must contain exactly {count} paragraphs.")

    default_level = normalized_level if normalized_level in ("beginner", "intermediate", "advanced") else "intermediate"
    return [_validate_paragraph(p, default_level=default_level) for p in paragraphs]
