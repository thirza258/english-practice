from __future__ import annotations

import csv
import logging
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from django.conf import settings

logger = logging.getLogger(__name__)

# Short PoS codes from CSV to human-readable names
POS_NAME_MAP: dict[str, str] = {
    "n": "noun",
    "v": "verb",
    "j": "adjective",
    "r": "adverb",
    "c": "conjunction",
    "i": "preposition",
    "d": "determiner",
    "p": "pronoun",
    "m": "modal",
    "a": "article",
}

# Domain full names
DOMAIN_NAME_MAP: dict[str, str] = {
    "Edu": "Education",
    "Sci": "Science & Technology",
    "Med": "Medicine & Health",
    "Law": "Law & Political Science",
    "Soc": "Social Sciences",
    "His": "History",
    "Hum": "Humanities",
    "Rel": "Philosophy & Religion",
    "Fin": "Business & Finance",
}


@dataclass(frozen=True)
class OxfordWord:
    word: str
    pos: str
    level: str  # B1, B2, C1, C2


@dataclass(frozen=True)
class AcademicWordEntry:
    fam_rank: int
    family: str
    word: str
    pos: str
    freq: int
    categ: str  # 'y' = core academic, 'r' = domain technical, 'x' = family member
    domain: str


@dataclass(frozen=True)
class AcademicWordFamily:
    fam_rank: int
    family: str
    fam_freq: int
    words: tuple[AcademicWordEntry, ...]


class VocabularyRepository:
    """Repository for Oxford 5000 (MD) and Academic Vocabulary List / AVL (CSV) datasets."""

    def __init__(self, source_dir: Path | None = None) -> None:
        if source_dir is None:
            source_dir = getattr(settings, "BASE_DIR", Path.cwd()) / "source"
        self.source_dir = Path(source_dir)
        self._oxford_words: list[OxfordWord] = []
        self._oxford_by_level: dict[str, list[OxfordWord]] = {"b1": [], "b2": [], "c1": [], "c2": []}
        self._oxford_by_word: dict[str, OxfordWord] = {}

        self._academic_entries: list[AcademicWordEntry] = []
        self._academic_families: list[AcademicWordFamily] = []
        self._academic_by_domain: dict[str, list[AcademicWordFamily]] = {}
        self._academic_by_word: dict[str, list[AcademicWordEntry]] = {}
        self._loaded: bool = False

    def ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._load_oxford_5000()
        self._load_academic_families()
        self._loaded = True

    def _load_oxford_5000(self) -> None:
        oxford_path = self.source_dir / "American_Oxford_5000.md"
        if not oxford_path.is_file():
            logger.warning("Oxford 5000 file not found at %s", oxford_path)
            return

        try:
            content = oxford_path.read_text(encoding="utf-8", errors="ignore")
            # Filter comments and header lines
            cleaned_lines = [
                line.strip()
                for line in content.splitlines()
                if line.strip() and not line.startswith("#") and not line.startswith("The Oxford")
            ]
            cleaned_text = " ".join(cleaned_lines)

            # Insert newline after each level indicator (B1, B2, C1, C2) to split cleanly
            text_with_newlines = re.sub(r"\b(B1|B2|C1|C2)\b", r"\1\n", cleaned_text)
            raw_entries = [l.strip() for l in text_with_newlines.splitlines() if l.strip()]

            words_list: list[OxfordWord] = []
            by_level: dict[str, list[OxfordWord]] = {"b1": [], "b2": [], "c1": [], "c2": []}
            by_word: dict[str, OxfordWord] = {}

            # Pattern matches: word (with optional pos/disambiguation) + PoS + Level
            line_pattern = re.compile(
                r"^(.+?)\s+((?:[a-z\./]+(?:\s*,\s*[a-z\./]+)*|\b[a-z\./]+\b)+)\s+(B1|B2|C1|C2)$",
                re.IGNORECASE,
            )

            for line in raw_entries:
                m = line_pattern.match(line)
                if not m:
                    continue
                w_raw, pos_raw, lvl_raw = m.group(1).strip(), m.group(2).strip(), m.group(3).strip().upper()
                w_clean = w_raw.strip("-").strip()
                if w_clean and lvl_raw:
                    entry = OxfordWord(word=w_clean, pos=pos_raw, level=lvl_raw)
                    words_list.append(entry)
                    by_level.setdefault(lvl_raw.lower(), []).append(entry)
                    by_word[w_clean.lower()] = entry

            self._oxford_words = words_list
            self._oxford_by_level = by_level
            self._oxford_by_word = by_word
            logger.info("Loaded %d Oxford 5000 words from MD.", len(words_list))
        except Exception as exc:
            logger.error("Failed to load Oxford 5000 vocabulary: %s", exc)

    def _load_academic_families(self) -> None:
        families_path = self.source_dir / "families-data.csv"
        if not families_path.is_file():
            logger.warning("Academic families CSV not found at %s", families_path)
            return

        try:
            entries: list[AcademicWordEntry] = []
            families_map: dict[str, list[AcademicWordEntry]] = {}
            fam_rank_map: dict[str, int] = {}
            fam_freq_map: dict[str, int] = {}
            by_word_map: dict[str, list[AcademicWordEntry]] = {}

            with families_path.open("r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    family = (row.get("family") or "").strip()
                    word = (row.get("word") or "").strip()
                    if not family or not word:
                        continue

                    fam_rank_str = (row.get("famRank") or "0").strip().replace(",", "")
                    fam_freq_str = (row.get("famFreq") or "0").strip().replace(",", "")
                    freq_str = (row.get("freq") or "0").strip().replace(",", "")

                    try:
                        fam_rank = int(fam_rank_str)
                    except ValueError:
                        fam_rank = 0

                    try:
                        fam_freq = int(fam_freq_str)
                    except ValueError:
                        fam_freq = 0

                    try:
                        freq = int(freq_str)
                    except ValueError:
                        freq = 0

                    pos = (row.get("PoS") or "").strip().lower()
                    categ = (row.get("categ") or "").strip().lower()
                    domain = (row.get("domain") or "").strip()

                    entry = AcademicWordEntry(
                        fam_rank=fam_rank,
                        family=family,
                        word=word,
                        pos=pos,
                        freq=freq,
                        categ=categ,
                        domain=domain,
                    )
                    entries.append(entry)
                    families_map.setdefault(family, []).append(entry)
                    by_word_map.setdefault(word.lower(), []).append(entry)
                    fam_rank_map[family] = fam_rank
                    fam_freq_map[family] = fam_freq

            academic_families: list[AcademicWordFamily] = []
            by_domain: dict[str, list[AcademicWordFamily]] = {}

            for family_name, word_entries in families_map.items():
                family_obj = AcademicWordFamily(
                    fam_rank=fam_rank_map.get(family_name, 0),
                    family=family_name,
                    fam_freq=fam_freq_map.get(family_name, 0),
                    words=tuple(word_entries),
                )
                academic_families.append(family_obj)

                # Map domains
                doms = {e.domain for e in word_entries if e.domain}
                for dom in doms:
                    for primary_dom in dom.split("+"):
                        clean_d = primary_dom.strip()
                        if clean_d:
                            by_domain.setdefault(clean_d, []).append(family_obj)

            academic_families.sort(key=lambda fam: fam.fam_rank)
            self._academic_entries = entries
            self._academic_families = academic_families
            self._academic_by_domain = by_domain
            self._academic_by_word = by_word_map
            logger.info("Loaded %d AVL word entries across %d families from CSV.", len(entries), len(academic_families))
        except Exception as exc:
            logger.error("Failed to load Academic Vocabulary List CSV: %s", exc)

    @property
    def oxford_words(self) -> list[OxfordWord]:
        self.ensure_loaded()
        return self._oxford_words

    @property
    def academic_families(self) -> list[AcademicWordFamily]:
        self.ensure_loaded()
        return self._academic_families

    @property
    def academic_entries(self) -> list[AcademicWordEntry]:
        self.ensure_loaded()
        return self._academic_entries

    def lookup_word(self, word: str) -> dict[str, Any]:
        """Look up a word in both Oxford 5000 and Academic Vocabulary List datasets."""
        self.ensure_loaded()
        w = word.strip().lower()
        oxford = self._oxford_by_word.get(w)
        academic = self._academic_by_word.get(w, [])

        return {
            "query": word,
            "oxford": (
                {"word": oxford.word, "pos": oxford.pos, "level": oxford.level}
                if oxford
                else None
            ),
            "academic_entries": [
                {
                    "family": e.family,
                    "word": e.word,
                    "pos": POS_NAME_MAP.get(e.pos, e.pos),
                    "freq": e.freq,
                    "categ": "core academic" if e.categ == "y" else "technical domain" if e.categ == "r" else "general member",
                    "domain": DOMAIN_NAME_MAP.get(e.domain, e.domain) if e.domain else "General Academic",
                    "fam_rank": e.fam_rank,
                }
                for e in academic
            ],
        }

    def get_oxford_sample(self, level: str = "all", count: int = 10) -> list[OxfordWord]:
        self.ensure_loaded()
        lvl = level.lower()
        if lvl in ("beginner", "a1", "a2"):
            # Beginner: B2 foundational items or base list
            pool = self._oxford_by_level.get("b2", [])
        elif lvl in ("intermediate", "b1", "b2"):
            pool = self._oxford_by_level.get("b2", [])
        elif lvl in ("advanced", "c1", "c2"):
            pool = self._oxford_by_level.get("c1", [])
        elif lvl == "ielts_8_9":
            # IELTS 8-9: Top-tier C1 words
            pool = self._oxford_by_level.get("c1", [])
        else:
            pool = self._oxford_words

        if not pool:
            pool = self._oxford_words
        if not pool:
            return []
        sample_size = min(count, len(pool))
        return random.sample(pool, sample_size)

    def get_academic_sample(
        self,
        level: str = "all",
        count: int = 5,
        domain: str | None = None,
    ) -> list[AcademicWordFamily]:
        self.ensure_loaded()
        lvl = level.lower()

        if domain and domain in self._academic_by_domain:
            pool = self._academic_by_domain[domain]
        elif lvl == "beginner":
            # Beginner: Top 50 most frequent foundational word families
            pool = self._academic_families[:50]
        elif lvl == "intermediate":
            # Intermediate: Core academic families rank 50 to 800 with core 'y' category
            pool = [fam for fam in self._academic_families[50:800] if any(w.categ == "y" for w in fam.words)]
        elif lvl in ("advanced", "ielts_8_9"):
            # Advanced / IELTS: Mid-to-high rank academic families with technical/domain or nuanced members
            pool = [
                fam
                for fam in self._academic_families[200:]
                if any(w.categ in ("y", "r") and (w.pos in ("j", "r", "v", "n") or w.domain) for w in fam.words)
            ]
        else:
            pool = self._academic_families

        if not pool:
            pool = self._academic_families
        if not pool:
            return []
        sample_size = min(count, len(pool))
        return random.sample(pool, sample_size)

    def format_prompt_vocabulary_context(
        self,
        level: str = "all",
        count: int = 8,
        mode: str = "sentence",
    ) -> str:
        """Format an authentic vocabulary context snippet from MD and CSV to inject into LLM prompts."""
        self.ensure_loaded()
        lvl = level.lower()

        oxford_sample = self.get_oxford_sample(level=lvl, count=count)
        academic_sample = self.get_academic_sample(level=lvl, count=max(4, count // 2))

        lines: list[str] = []

        if mode == "paragraph":
            lines.append("Source Academic Vocabulary & Word Families (from AVL CSV & Oxford 5000 MD):")
            for fam in academic_sample:
                dom_tags = {DOMAIN_NAME_MAP.get(e.domain, e.domain) for e in fam.words if e.domain}
                dom_str = f" [Domain: {', '.join(sorted(dom_tags))}]" if dom_tags else ""
                core_words = [f"{e.word} ({POS_NAME_MAP.get(e.pos, e.pos)})" for e in fam.words[:4]]
                lines.append(f"- Family [{fam.family}]{dom_str}: {', '.join(core_words)}")

            if oxford_sample:
                ox_items = [f"{item.word} ({item.pos}, CEFR {item.level})" for item in oxford_sample[:6]]
                lines.append(f"- Target Register Lexicon: {', '.join(ox_items)}")

            lines.append(
                "Prompt Guideline: Anchor the paragraph topic around the above academic word families and domain themes, "
                "weaving them naturally into the discourse so that the cloze choices reflect authentic academic English."
            )
        else:
            lines.append("Source Vocabulary & Lexicon Context (from Oxford 5000 MD & Academic Vocabulary List CSV):")
            if lvl != "beginner" and oxford_sample:
                ox_items = [f"{item.word} ({item.pos}, {item.level})" for item in oxford_sample]
                lines.append(f"- Target Oxford 5000 Words: {', '.join(ox_items)}")

            if academic_sample:
                avl_items = []
                for fam in academic_sample:
                    top_derivs = [w.word for w in fam.words if w.categ in ("y", "r")][:3] or [fam.family]
                    avl_items.append(f"[{fam.family}: {', '.join(top_derivs)}]")
                lines.append(f"- Academic Word Families: {'; '.join(avl_items)}")

            lines.append(
                "Prompt Guideline: Where grammatically fitting, use target vocabulary words or derivatives from "
                "the above reference sets as context words, answer options, or sentence stems."
            )

        return "\n".join(lines)


# Global singleton instance for easy import
vocabulary_repo = VocabularyRepository()
