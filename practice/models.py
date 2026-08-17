from __future__ import annotations

import hashlib
import json
from typing import Iterable, Sequence

from django.db import models

from .question_bank import QuestionBlueprint


class QuestionBankQuestion(models.Model):
    topic = models.CharField(max_length=255)
    question = models.TextField()
    correct_answer = models.TextField()
    distractors = models.JSONField(default=list)
    rule = models.TextField()
    explanation = models.TextField()
    sentence_explanation = models.TextField()
    secondary_topics = models.JSONField(default=list, blank=True)
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
    ) -> str:
        payload = {
            "topic": topic.strip(),
            "question": question.strip(),
            "correct_answer": correct_answer.strip(),
            "distractors": [choice.strip() for choice in distractors],
            "secondary_topics": [topic.strip() for topic in (secondary_topics or [])],
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
        )

    @classmethod
    def seed_from_static_bank(cls) -> int:
        if cls.objects.exists():
            return 0

        from .question_bank import QUESTION_BANK

        entries = [cls.from_blueprint(blueprint, source="seed") for blueprint in QUESTION_BANK]
        cls.objects.bulk_create(entries, ignore_conflicts=True)
        return len(entries)

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
        exclude_hashes: Iterable[str] | None = None,
    ) -> list["QuestionBankQuestion"]:
        if count <= 0:
            return []

        queryset = cls.objects.all()
        if exclude_hashes:
            queryset = queryset.exclude(content_hash__in=list(exclude_hashes))
        return list(queryset.order_by("?")[:count])


class TestSession(models.Model):
    session_id = models.CharField(max_length=32, unique=True, db_index=True)
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
            "total_questions": self.total_questions,
            "current_index": self.current_index,
            "score": self.score,
            "completed": self.completed,
            "questions": self.questions,
        }

    @classmethod
    def load_by_id(cls, session_id: str) -> "TestSession" | None:
        return cls.objects.filter(session_id=session_id).first()
