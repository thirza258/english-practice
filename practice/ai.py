from __future__ import annotations

import json
import logging
import os
import time
from typing import Any, Callable, TypeVar

from openai import OpenAI

from .question_bank import BlankBlueprint, ParagraphBlueprint, QUESTION_BANK, QuestionBlueprint
from .vocabulary import vocabulary_repo


logger = logging.getLogger(__name__)

MAX_GENERATION_ATTEMPTS = 5
GENERATION_RETRY_DELAY_SECONDS = 1.5

T = TypeVar("T")

OPENROUTER_BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_APP_TITLE = os.environ.get("OPENROUTER_APP_TITLE", "English Practice Diagnostic")
OPENROUTER_REFERER = os.environ.get("OPENROUTER_REFERER")


def _generate_with_retries(generate_fn: Callable[[], T], label: str) -> T:
    """Run an AI generation up to MAX_GENERATION_ATTEMPTS times, then raise.

    After the final failure the caller (services) falls back to the database
    question bank, so a provider outage never blocks a test.
    """
    last_error: Exception | None = None
    for attempt in range(1, MAX_GENERATION_ATTEMPTS + 1):
        try:
            return generate_fn()
        except RuntimeError:
            # Configuration error (e.g. missing OPENROUTER_API_KEY) — retrying will not help.
            raise
        except Exception as exc:
            last_error = exc
            logger.warning(
                "AI %s generation attempt %d/%d failed: %s",
                label,
                attempt,
                MAX_GENERATION_ATTEMPTS,
                exc,
            )
            if attempt < MAX_GENERATION_ATTEMPTS:
                time.sleep(GENERATION_RETRY_DELAY_SECONDS)
    logger.error(
        "AI %s generation failed after %d attempts; using database bank only.",
        label,
        MAX_GENERATION_ATTEMPTS,
    )
    raise last_error  # type: ignore[misc]

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
    vocab_context = vocabulary_repo.format_prompt_vocabulary_context(
        level=level_key,
        count=max(total_questions, 8),
        mode="sentence",
    )

    system = (
        "You generate English grammar diagnostic questions for a web app. "
        "Return only valid JSON. Do not use markdown. "
        "Every question must have exactly one correct answer, four plausible distractors, "
        "a hidden grammar topic, an English level (beginner, intermediate, advanced, or ielts_8_9), "
        "a short rule, a concise explanation, and a sentence-based explanation. "
        "The visible question text must not reveal the topic."
    )
    user = f"""
Generate exactly {total_questions} multiple-choice grammar questions.

Difficulty & Level requirement:
{guidance}

Vocabulary & Lexicon Grounding:
{vocab_context}

Rules:
- Use only topics from this list.
- Topics may repeat, but the set should feel varied.
- Each question must have exactly one clearly correct answer.
- Each question must include four distinct distractors.
- The correct answer should be the exact value of "correct_answer".
- Do not include answer letters in options or answers.
- Do not reveal the topic in the question text.
- Set "level" for each question to "beginner", "intermediate", "advanced", or "ielts_8_9".
- Keep questions natural, accurate, and concise.

Allowed topics:
{topics}

Return JSON in this shape:
{{
  "questions": [
    {{
      "topic": "one of the allowed topics",
      "level": "beginner | intermediate | advanced | ielts_8_9",
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
    def _attempt() -> list[QuestionBlueprint]:
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

        default_level = normalized_level if normalized_level in ("beginner", "intermediate", "advanced", "ielts_8_9") else "intermediate"
        blueprints = [_validate_question(item, default_level=default_level) for item in questions]
        if len({blueprint.question.strip().lower() for blueprint in blueprints}) != total_questions:
            raise ValueError("AI output must contain unique question text.")
        return blueprints

    return _generate_with_retries(_attempt, "question")


# -----------------------------------------------------------------------------
# PARAGRAPH CLOZE / BUILDER AI GENERATION
# -----------------------------------------------------------------------------

def _paragraph_prompt(count: int, level: str = "all") -> list[dict[str, str]]:
    level_key = level.lower() if level.lower() in PARAGRAPH_LEVEL_GUIDANCE else "all"
    guidance = PARAGRAPH_LEVEL_GUIDANCE[level_key]
    vocab_context = vocabulary_repo.format_prompt_vocabulary_context(
        level=level_key,
        count=max(count * 3, 8),
        mode="paragraph",
    )

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

Thematic Academic Vocabulary & Word Families Context (from Academic Vocabulary List CSV & Oxford 5000 MD):
{vocab_context}

Rules:
- Each paragraph must be cohesive, natural English with exactly 3 blanks marked as [1], [2], and [3].
- Each blank must have exactly 1 clearly correct answer and exactly 4 plausible distractors.
- For each blank, specify topic, rule, explanation, and distractors.
- Provide "full_text" (the complete paragraph without blanks) and "paragraph_explanation" (explaining paragraph structure, transitions, and cohesion).
- Set "level" to "beginner", "intermediate", "advanced", or "ielts_8_9".

Return JSON in this shape:
{{
  "paragraphs": [
    {{
      "title": "Topic title",
      "level": "beginner | intermediate | advanced | ielts_8_9",
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
    def _attempt() -> list[ParagraphBlueprint]:
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

        default_level = normalized_level if normalized_level in ("beginner", "intermediate", "advanced", "ielts_8_9") else "intermediate"
        return [_validate_paragraph(p, default_level=default_level) for p in paragraphs]

    return _generate_with_retries(_attempt, "paragraph")


# -----------------------------------------------------------------------------
# IELTS WRITING EVALUATION
# -----------------------------------------------------------------------------
#
# Token budget: every countable fact (length, repetition, clause ratios, linker
# coverage, mechanics) is measured in ``practice.nlp`` and handed over as a
# single digest line, so the model is paid only for judgement. The essay is
# truncated, the reply uses short keys, and the output is capped.

WRITING_MODEL = os.environ.get("OPENROUTER_WRITING_MODEL") or OPENROUTER_MODEL
WRITING_MAX_ESSAY_WORDS = int(os.environ.get("WRITING_MAX_ESSAY_WORDS", "450"))
WRITING_MAX_OUTPUT_TOKENS = int(os.environ.get("WRITING_MAX_OUTPUT_TOKENS", "700"))
WRITING_AI_TIMEOUT = float(os.environ.get("WRITING_AI_TIMEOUT", "45"))

WRITING_LEVEL_TARGET: dict[str, str] = {
    "beginner": "A1-A2 learner: reward clear simple sentences; do not demand academic range.",
    "intermediate": "B1-B2 learner: expect clear paragraphing and some complex sentences.",
    "advanced": "C1-C2 learner: expect sustained argument and precise, varied lexis.",
    "ielts_8_9": "Band 8-9 candidate: expect rare precise lexis and flexible, accurate syntax.",
    "all": "Mixed level: apply the standard descriptors without adjustment.",
}

_WRITING_SYSTEM = (
    "You are an IELTS writing examiner. Score the response against the four Writing Task 2 band "
    "descriptors using whole or half bands from 1 to 9. Be strict and consistent.\n"
    "The METRICS line has already been measured programmatically: trust it and never recount "
    "words, sentences, or repetitions.\n"
    "Weight two things heavily: lexical range (variety and precision of vocabulary, penalising "
    "repeated basic words) and structure (paragraph organisation, topic sentences, and correct, "
    "varied sentence construction).\n"
    "Quote only text that actually appears in the response.\n"
    "Return only JSON, no markdown, in exactly this shape:\n"
    '{"tr":[band,"comment"],"cc":[band,"comment"],"lr":[band,"comment"],"gra":[band,"comment"],'
    '"str":["strength"],"imp":["improvement"],'
    '"fix":[{"o":"original phrase","c":"corrected","w":"why"}],'
    '"voc":[{"b":"basic word used","u":"stronger replacement"}]}\n'
    "Limits: each comment at most 25 words; str and imp at most 3 items each; "
    "fix at most 5 items; voc at most 6 items; every string plain text."
)


def _writing_prompt(
    *,
    essay: str,
    digest: str,
    local_bands: dict[str, float],
    task_title: str,
    task_prompt: str,
    level: str,
) -> list[dict[str, str]]:
    level_key = level.lower() if level.lower() in WRITING_LEVEL_TARGET else "all"

    words = essay.split()
    if len(words) > WRITING_MAX_ESSAY_WORDS:
        essay = " ".join(words[:WRITING_MAX_ESSAY_WORDS]) + " [...truncated]"

    prior = " ".join(f"{key}={value}" for key, value in sorted(local_bands.items()))

    user = (
        f"LEVEL: {WRITING_LEVEL_TARGET[level_key]}\n"
        f"TASK: {task_title} - {task_prompt}\n"
        f"METRICS: {digest}\n"
        f"STATISTICAL PRIOR (from metrics only, may be wrong about content): {prior}\n"
        "RESPONSE:\n"
        f"{essay}"
    )

    return [
        {"role": "system", "content": _WRITING_SYSTEM},
        {"role": "user", "content": user},
    ]


_CRITERION_KEYS = (
    ("tr", "task_response"),
    ("cc", "coherence_cohesion"),
    ("lr", "lexical_resource"),
    ("gra", "grammatical_range"),
)


def _clean_text(value: Any, limit: int = 400) -> str:
    return " ".join(str(value or "").split())[:limit]


def _criterion_pair(raw: Any) -> tuple[float | None, str]:
    """Accept ``[band, comment]`` and also ``{"band": .., "comment": ..}``."""

    band: Any = None
    comment: Any = ""

    if isinstance(raw, (list, tuple)) and raw:
        band = raw[0]
        comment = raw[1] if len(raw) > 1 else ""
    elif isinstance(raw, dict):
        band = raw.get("band", raw.get("b"))
        comment = raw.get("comment", raw.get("c", ""))
    elif isinstance(raw, (int, float, str)):
        band = raw

    try:
        band_value: float | None = float(band)
    except (TypeError, ValueError):
        band_value = None

    return band_value, _clean_text(comment, 300)


def _validate_writing_report(data: dict[str, Any]) -> dict[str, Any]:
    from .nlp import round_half_band

    bands: dict[str, float] = {}
    comments: dict[str, str] = {}
    for short_key, name in _CRITERION_KEYS:
        band, comment = _criterion_pair(data.get(short_key))
        if band is None:
            raise ValueError(f"AI writing report is missing a band for {name}.")
        bands[name] = round_half_band(band)
        comments[name] = comment

    def string_list(key: str, limit: int) -> list[str]:
        raw = data.get(key) or []
        if not isinstance(raw, list):
            return []
        return [_clean_text(item, 240) for item in raw if _clean_text(item, 240)][:limit]

    corrections = []
    for item in (data.get("fix") or [])[:5]:
        if not isinstance(item, dict):
            continue
        original = _clean_text(item.get("o") or item.get("original"), 240)
        corrected = _clean_text(item.get("c") or item.get("corrected"), 240)
        if not original or not corrected:
            continue
        corrections.append(
            {
                "original": original,
                "corrected": corrected,
                "why": _clean_text(item.get("w") or item.get("why"), 240),
            }
        )

    upgrades = []
    for item in (data.get("voc") or [])[:6]:
        if not isinstance(item, dict):
            continue
        basic = _clean_text(item.get("b") or item.get("basic"), 80)
        stronger = _clean_text(item.get("u") or item.get("upgrade"), 160)
        if basic and stronger:
            upgrades.append({"basic": basic, "stronger": stronger})

    return {
        "bands": bands,
        "comments": comments,
        "strengths": string_list("str", 3),
        "improvements": string_list("imp", 3),
        "corrections": corrections,
        "vocabulary_upgrades": upgrades,
    }


def evaluate_writing(
    *,
    essay: str,
    digest: str,
    local_bands: dict[str, float],
    task_title: str,
    task_prompt: str,
    level: str = "all",
) -> dict[str, Any]:
    """Ask the model for band scores and targeted feedback only.

    Raises on any failure so the caller can fall back to the local assessment.
    """

    client = _client()
    response = client.chat.completions.create(
        model=WRITING_MODEL,
        messages=_writing_prompt(
            essay=essay,
            digest=digest,
            local_bands=local_bands,
            task_title=task_title,
            task_prompt=task_prompt,
            level=level,
        ),
        temperature=0.2,
        max_tokens=WRITING_MAX_OUTPUT_TOKENS,
        response_format={"type": "json_object"},
        timeout=WRITING_AI_TIMEOUT,
    )

    report = _validate_writing_report(json.loads(response.choices[0].message.content or "{}"))

    usage = getattr(response, "usage", None)
    report["usage"] = {
        "prompt_tokens": getattr(usage, "prompt_tokens", None),
        "completion_tokens": getattr(usage, "completion_tokens", None),
        "total_tokens": getattr(usage, "total_tokens", None),
    }
    report["model"] = WRITING_MODEL
    return report

