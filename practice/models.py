from __future__ import annotations

import hashlib
import json
from typing import Iterable, Sequence

from django.db import models

from .question_bank import BlankBlueprint, ParagraphBlueprint, QuestionBlueprint


class QuestionBankQuestion(models.Model):
    topic = models.CharField(max_length=255)
    question = models.TextField()
    correct_answer = models.TextField()
    distractors = models.JSONField(default=list)
    rule = models.TextField()
    explanation = models.TextField()
    sentence_explanation = models.TextField()
    secondary_topics = models.JSONField(default=list, blank=True)
    level = models.CharField(max_length=32, default="intermediate", db_index=True)
    source = models.CharField(max_length=32, default="seed")
    generation_metadata = models.JSONField(default=dict, blank=True)
    content_hash = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    @staticmethod
    def fingerprint(
        *,
        topic: str,
        question: str,
        correct_answer: str,
        distractors: Sequence[str],
        secondary_topics: Sequence[str] | None = None,
        level: str = "intermediate",
    ) -> str:
        payload = {
            "topic": topic.strip(),
            "question": question.strip(),
            "correct_answer": correct_answer.strip(),
            "distractors": [choice.strip() for choice in distractors],
            "secondary_topics": [topic.strip() for topic in (secondary_topics or [])],
            "level": level.strip().lower(),
        }
        serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    @classmethod
    def from_blueprint(
        cls,
        blueprint: QuestionBlueprint,
        *,
        source: str = "openrouter",
        generation_metadata: dict | None = None,
    ) -> "QuestionBankQuestion":
        content_hash = cls.fingerprint(
            topic=blueprint.topic,
            question=blueprint.question,
            correct_answer=blueprint.correct_answer,
            distractors=blueprint.distractors,
            secondary_topics=blueprint.secondary_topics,
            level=blueprint.level,
        )
        return cls(
            topic=blueprint.topic,
            question=blueprint.question,
            correct_answer=blueprint.correct_answer,
            distractors=list(blueprint.distractors),
            rule=blueprint.rule,
            explanation=blueprint.explanation,
            sentence_explanation=blueprint.sentence_explanation,
            secondary_topics=list(blueprint.secondary_topics),
            level=blueprint.level,
            source=source,
            generation_metadata=generation_metadata or {},
            content_hash=content_hash,
        )

    def to_blueprint(self) -> QuestionBlueprint:
        return QuestionBlueprint(
            topic=self.topic,
            question=self.question,
            correct_answer=self.correct_answer,
            distractors=tuple(str(choice) for choice in self.distractors),
            rule=self.rule,
            explanation=self.explanation,
            sentence_explanation=self.sentence_explanation,
            secondary_topics=tuple(str(topic) for topic in self.secondary_topics),
            level=self.level,
        )

    @classmethod
    def seed_from_static_bank(cls) -> int:
        from .question_bank import QUESTION_BANK

        created_count = 0
        for blueprint in QUESTION_BANK:
            entry = cls.from_blueprint(blueprint, source="seed")
            _, created = cls.objects.get_or_create(
                content_hash=entry.content_hash,
                defaults={
                    "topic": entry.topic,
                    "question": entry.question,
                    "correct_answer": entry.correct_answer,
                    "distractors": entry.distractors,
                    "rule": entry.rule,
                    "explanation": entry.explanation,
                    "sentence_explanation": entry.sentence_explanation,
                    "secondary_topics": entry.secondary_topics,
                    "level": entry.level,
                    "source": entry.source,
                    "generation_metadata": entry.generation_metadata,
                },
            )
            if created:
                created_count += 1
        return created_count

    @classmethod
    def save_blueprints(
        cls,
        blueprints: Iterable[QuestionBlueprint],
        *,
        source: str = "openrouter",
        generation_metadata: dict | None = None,
    ) -> list["QuestionBankQuestion"]:
        saved: list[QuestionBankQuestion] = []
        for blueprint in blueprints:
            entry = cls.from_blueprint(
                blueprint,
                source=source,
                generation_metadata=generation_metadata,
            )
            obj, _ = cls.objects.get_or_create(
                content_hash=entry.content_hash,
                defaults={
                    "topic": entry.topic,
                    "question": entry.question,
                    "correct_answer": entry.correct_answer,
                    "distractors": entry.distractors,
                    "rule": entry.rule,
                    "explanation": entry.explanation,
                    "sentence_explanation": entry.sentence_explanation,
                    "secondary_topics": entry.secondary_topics,
                    "level": entry.level,
                    "source": entry.source,
                    "generation_metadata": entry.generation_metadata,
                },
            )
            saved.append(obj)
        return saved

    @classmethod
    def random_sample(
        cls,
        count: int,
        *,
        level: str | None = None,
        exclude_hashes: Iterable[str] | None = None,
    ) -> list["QuestionBankQuestion"]:
        if count <= 0:
            return []

        queryset = cls.objects.all()
        if exclude_hashes:
            queryset = queryset.exclude(content_hash__in=list(exclude_hashes))

        if level and level.lower() != "all":
            level_queryset = queryset.filter(level=level.lower())
            results = list(level_queryset.order_by("?")[:count])
            if len(results) >= count:
                return results
            remaining = count - len(results)
            seen_ids = {item.id for item in results}
            extra = list(queryset.exclude(id__in=seen_ids).order_by("?")[:remaining])
            return [*results, *extra]

        return list(queryset.order_by("?")[:count])


class ParagraphBankQuestion(models.Model):
    title = models.CharField(max_length=255)
    text_with_blanks = models.TextField()
    blanks = models.JSONField(default=list)
    level = models.CharField(max_length=32, default="intermediate", db_index=True)
    full_text = models.TextField()
    paragraph_explanation = models.TextField()
    source = models.CharField(max_length=32, default="seed")
    generation_metadata = models.JSONField(default=dict, blank=True)
    content_hash = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    @staticmethod
    def fingerprint(
        *,
        text_with_blanks: str,
        blanks: Sequence[dict],
        level: str = "intermediate",
    ) -> str:
        payload = {
            "text_with_blanks": text_with_blanks.strip(),
            "blanks": [
                {
                    "blank_id": b.get("blank_id"),
                    "topic": str(b.get("topic", "")).strip(),
                    "correct_answer": str(b.get("correct_answer", "")).strip(),
                    "distractors": [str(d).strip() for d in b.get("distractors", [])],
                }
                for b in blanks
            ],
            "level": level.strip().lower(),
        }
        serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    @classmethod
    def from_blueprint(
        cls,
        blueprint: ParagraphBlueprint,
        *,
        source: str = "openrouter",
        generation_metadata: dict | None = None,
    ) -> "ParagraphBankQuestion":
        blanks_payload = [
            {
                "blank_id": blank.blank_id,
                "topic": blank.topic,
                "correct_answer": blank.correct_answer,
                "distractors": list(blank.distractors),
                "rule": blank.rule,
                "explanation": blank.explanation,
                "secondary_topics": list(blank.secondary_topics),
            }
            for blank in blueprint.blanks
        ]
        content_hash = cls.fingerprint(
            text_with_blanks=blueprint.text_with_blanks,
            blanks=blanks_payload,
            level=blueprint.level,
        )
        return cls(
            title=blueprint.title,
            text_with_blanks=blueprint.text_with_blanks,
            blanks=blanks_payload,
            level=blueprint.level,
            full_text=blueprint.full_text,
            paragraph_explanation=blueprint.paragraph_explanation,
            source=source,
            generation_metadata=generation_metadata or {},
            content_hash=content_hash,
        )

    def to_blueprint(self) -> ParagraphBlueprint:
        blanks = [
            BlankBlueprint(
                blank_id=b["blank_id"],
                topic=b["topic"],
                correct_answer=b["correct_answer"],
                distractors=tuple(str(d) for d in b["distractors"]),
                rule=b["rule"],
                explanation=b["explanation"],
                secondary_topics=tuple(str(t) for t in b.get("secondary_topics", ())),
            )
            for b in self.blanks
        ]
        return ParagraphBlueprint(
            title=self.title,
            text_with_blanks=self.text_with_blanks,
            blanks=tuple(blanks),
            level=self.level,
            full_text=self.full_text,
            paragraph_explanation=self.paragraph_explanation,
        )

    @classmethod
    def seed_from_static_bank(cls) -> int:
        from .question_bank import PARAGRAPH_BANK

        created_count = 0
        for blueprint in PARAGRAPH_BANK:
            entry = cls.from_blueprint(blueprint, source="seed")
            _, created = cls.objects.get_or_create(
                content_hash=entry.content_hash,
                defaults={
                    "title": entry.title,
                    "text_with_blanks": entry.text_with_blanks,
                    "blanks": entry.blanks,
                    "level": entry.level,
                    "full_text": entry.full_text,
                    "paragraph_explanation": entry.paragraph_explanation,
                    "source": entry.source,
                    "generation_metadata": entry.generation_metadata,
                },
            )
            if created:
                created_count += 1
        return created_count

    @classmethod
    def save_blueprints(
        cls,
        blueprints: Iterable[ParagraphBlueprint],
        *,
        source: str = "openrouter",
        generation_metadata: dict | None = None,
    ) -> list["ParagraphBankQuestion"]:
        saved: list[ParagraphBankQuestion] = []
        for blueprint in blueprints:
            entry = cls.from_blueprint(
                blueprint,
                source=source,
                generation_metadata=generation_metadata,
            )
            obj, _ = cls.objects.get_or_create(
                content_hash=entry.content_hash,
                defaults={
                    "title": entry.title,
                    "text_with_blanks": entry.text_with_blanks,
                    "blanks": entry.blanks,
                    "level": entry.level,
                    "full_text": entry.full_text,
                    "paragraph_explanation": entry.paragraph_explanation,
                    "source": entry.source,
                    "generation_metadata": entry.generation_metadata,
                },
            )
            saved.append(obj)
        return saved

    @classmethod
    def random_sample(
        cls,
        count: int,
        *,
        level: str | None = None,
        exclude_hashes: Iterable[str] | None = None,
    ) -> list["ParagraphBankQuestion"]:
        if count <= 0:
            return []

        queryset = cls.objects.all()
        if exclude_hashes:
            queryset = queryset.exclude(content_hash__in=list(exclude_hashes))

        if level and level.lower() != "all":
            level_queryset = queryset.filter(level=level.lower())
            results = list(level_queryset.order_by("?")[:count])
            if len(results) >= count:
                return results
            remaining = count - len(results)
            seen_ids = {item.id for item in results}
            extra = list(queryset.exclude(id__in=seen_ids).order_by("?")[:remaining])
            return [*results, *extra]

        return list(queryset.order_by("?")[:count])


class TestSession(models.Model):
    session_id = models.CharField(max_length=32, unique=True, db_index=True)
    test_type = models.CharField(max_length=32, default="sentence", db_index=True)
    level = models.CharField(max_length=32, default="all", db_index=True)
    total_questions = models.PositiveIntegerField(default=10)
    current_index = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    questions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-id"]

    @classmethod
    def create_from_state(cls, state: dict) -> "TestSession":
        obj, _ = cls.objects.update_or_create(
            session_id=state["id"],
            defaults={
                "test_type": state.get("test_type") or state.get("mode") or "sentence",
                "level": state.get("level", "all"),
                "total_questions": state["total_questions"],
                "current_index": state["current_index"],
                "score": state["score"],
                "completed": state["completed"],
                "questions": state["questions"],
            },
        )
        return obj

    def to_state(self) -> dict:
        return {
            "id": self.session_id,
            "test_type": self.test_type,
            "mode": self.test_type,
            "level": self.level,
            "total_questions": self.total_questions,
            "current_index": self.current_index,
            "score": self.score,
            "completed": self.completed,
            "questions": self.questions,
        }

    @classmethod
    def load_by_id(cls, session_id: str) -> "TestSession" | None:
        return cls.objects.filter(session_id=session_id).first()
