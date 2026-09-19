"""Shared curriculum types; slugs remain stable so saved work stays attached."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Section:
    title: str
    text: str


@dataclass(frozen=True)
class Example:
    before: str
    after: str
    explanation: str


@dataclass(frozen=True)
class Question:
    prompt: str
    options: tuple[str, ...]
    correct: int
    explanation: str


@dataclass(frozen=True)
class Assignment:
    prompt: str
    min_words: int
    checklist: tuple[str, ...]
    sample: str
    label: str = "Your writing"


@dataclass(frozen=True)
class Activity:
    kind: str
    title: str
    text: str
    seconds: int = 0
    preparation_seconds: int = 0
    map_rows: tuple[tuple[str, str, str], ...] = ()


@dataclass(frozen=True)
class Lesson:
    slug: str
    title: str
    minutes: int
    goal: str
    sections: tuple[Section, ...]
    example: Example
    questions: tuple[Question, ...]
    assignment: Assignment
    skill: str = ""
    activity: Activity | None = None
    level: str = ""
    technique: str = ""


@dataclass(frozen=True)
class Course:
    slug: str
    title: str
    category: str
    level: str
    description: str
    outcomes: tuple[str, ...]
    project: str
    lessons: tuple[Lesson, ...]
    resources: tuple[tuple[str, str], ...]
    practice_level: str = ""
    skill: str = ""
    strategy: tuple[Section, ...] = ()

    @property
    def is_ielts(self) -> bool:
        return bool(self.skill or self.practice_level)

    @property
    def minutes(self) -> int:
        return sum(lesson.minutes for lesson in self.lessons)
