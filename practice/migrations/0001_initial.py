from __future__ import annotations

import hashlib
import json

from django.db import migrations, models


def _fingerprint(topic, question, correct_answer, distractors, secondary_topics=None):
    payload = {
        "topic": topic.strip(),
        "question": question.strip(),
        "correct_answer": correct_answer.strip(),
        "distractors": [choice.strip() for choice in distractors],
        "secondary_topics": [topic.strip() for topic in (secondary_topics or [])],
    }
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def seed_question_bank(apps, schema_editor):
    QuestionBankQuestion = apps.get_model("practice", "QuestionBankQuestion")

    from practice.question_bank import QUESTION_BANK

    entries = []
    for blueprint in QUESTION_BANK:
        entries.append(
            QuestionBankQuestion(
                topic=blueprint.topic,
                question=blueprint.question,
                correct_answer=blueprint.correct_answer,
                distractors=list(blueprint.distractors),
                rule=blueprint.rule,
                explanation=blueprint.explanation,
                sentence_explanation=blueprint.sentence_explanation,
                secondary_topics=list(blueprint.secondary_topics),
                source="seed",
                generation_metadata={},
                content_hash=_fingerprint(
                    blueprint.topic,
                    blueprint.question,
                    blueprint.correct_answer,
                    blueprint.distractors,
                    blueprint.secondary_topics,
                ),
            )
        )

    QuestionBankQuestion.objects.bulk_create(entries, ignore_conflicts=True)


def unseed_question_bank(apps, schema_editor):
    QuestionBankQuestion = apps.get_model("practice", "QuestionBankQuestion")
    QuestionBankQuestion.objects.all().delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="QuestionBankQuestion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("topic", models.CharField(max_length=255)),
                ("question", models.TextField()),
                ("correct_answer", models.TextField()),
                ("distractors", models.JSONField(default=list)),
                ("rule", models.TextField()),
                ("explanation", models.TextField()),
                ("sentence_explanation", models.TextField()),
                ("secondary_topics", models.JSONField(blank=True, default=list)),
                ("source", models.CharField(default="seed", max_length=32)),
                ("generation_metadata", models.JSONField(blank=True, default=dict)),
                ("content_hash", models.CharField(db_index=True, max_length=64, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-created_at", "-id"],
            },
        ),
        migrations.RunPython(seed_question_bank, unseed_question_bank),
    ]
