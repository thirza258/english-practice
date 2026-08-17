from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("practice", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestSession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_id", models.CharField(db_index=True, max_length=32, unique=True)),
                ("total_questions", models.PositiveIntegerField(default=10)),
                ("current_index", models.PositiveIntegerField(default=0)),
                ("score", models.PositiveIntegerField(default=0)),
                ("completed", models.BooleanField(default=False)),
                ("questions", models.JSONField(default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-updated_at", "-id"],
            },
        ),
    ]
