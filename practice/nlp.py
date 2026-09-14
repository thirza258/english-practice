"""Local linguistic analysis of a learner's writing.

Everything that can be counted, measured, or matched is computed here with
NLTK (and spaCy when it is installed) so the language model is never asked to
count words, sentences, or repetitions. The model receives a short digest of
these numbers and spends its tokens on judgement alone.

Every optional dependency is probed lazily and degrades to a pure-regex
implementation, so the app works with nothing but the standard library.
"""

from __future__ import annotations

import math
import os
import re
from collections import Counter
from typing import Any, Sequence


# -----------------------------------------------------------------------------
# OPTIONAL DEPENDENCY PLUMBING
# -----------------------------------------------------------------------------

_NLTK_SENT: Any = None
_SPACY_NLP: Any = None
_SPACY_LOADED = False


def _flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _nltk_sentence_tokenizer() -> Any:
    """Return NLTK's ``sent_tokenize``, or ``None`` when it cannot be used.

    NLTK 3.9+ resolves ``punkt_tab`` while older releases resolve ``punkt``, and
    either corpus may be absent, so the tokenizer is probed with a real call
    before being cached.

    Only sentence segmentation comes from NLTK. Words are always counted with
    ``WORD_RE`` so that the count - which drives the minimum-length rule and the
    Task Response cap - is identical in every deployment and matches the live
    counter in the browser.
    """

    global _NLTK_SENT
    if _NLTK_SENT is not None:
        return _NLTK_SENT or None

    _NLTK_SENT = False
    if _flag("WRITING_DISABLE_NLTK"):
        return None

    try:
        from nltk.tokenize import sent_tokenize

        sent_tokenize("A probe sentence. And a second one.")
    except Exception:
        return None

    _NLTK_SENT = sent_tokenize
    return sent_tokenize


FALLBACK_STOPWORDS = frozenset(
    """
    a about above after again all am an and any are as at be because been before being below between
    both but by can cannot could did do does doing down during each few for from further had has have
    having he her here hers him his how i if in into is it its itself just me more most my no nor not
    of off on once only or other our ours out over own same she should so some such than that the
    their theirs them themselves then there these they this those through to too under until up very
    was we were what when where which while who whom why will with would you your yours
    """.split()
)

_STOPWORDS: Any = None


def _stopwords() -> frozenset[str]:
    """NLTK's English stopwords when the corpus is present, else a fallback."""

    global _STOPWORDS
    if _STOPWORDS is not None:
        return _STOPWORDS

    _STOPWORDS = FALLBACK_STOPWORDS
    if not _flag("WRITING_DISABLE_NLTK"):
        try:
            from nltk.corpus import stopwords

            words = set(stopwords.words("english"))
            if words:
                _STOPWORDS = frozenset(words | set(FALLBACK_STOPWORDS))
        except Exception:
            pass
    return _STOPWORDS


def _spacy_nlp() -> Any:
    """Load the spaCy pipeline once per worker, on first use only."""

    global _SPACY_NLP, _SPACY_LOADED
    if _SPACY_LOADED:
        return _SPACY_NLP

    _SPACY_LOADED = True
    if _flag("WRITING_DISABLE_SPACY"):
        return None

    try:
        import spacy

        _SPACY_NLP = spacy.load(os.environ.get("SPACY_MODEL", "en_core_web_sm"), exclude=["ner"])
    except Exception:
        _SPACY_NLP = None
    return _SPACY_NLP


# -----------------------------------------------------------------------------
# REFERENCE WORD LISTS
# -----------------------------------------------------------------------------

# The most frequent words of everyday English. Writing built mainly from this
# set is what IELTS calls a limited lexical resource, so the share of words
# *outside* it is a usable proxy for vocabulary range.
CORE_WORDS = frozenset(
    """
    a about after again all also always am an and another any are around as ask at away back be
    because been before being below best better between big both but buy by call came can come
    could day days did different do does doing done down each early eat end enough even ever every
    example far feel few find first for form found from get give go going good got great had happy
    has have he help her here high him his home how however i if important in into is it its just
    keep kind know last late learn leave left less let life like little live long look lot made
    make man many may me mean might money more most move much must my name near need never new next
    nice no not now number of off often old on once one only or other our out over own part people
    place play point put really right said same saw say see seem she should show side since small so
    some something soon still such take talk tell than that the their them then there these they
    thing things think this those thought three through time times to today together too took two
    under until up upon us use used usually very want was way we week well went were what when where
    which while who why will with without word work world would year years yes yet you young your
    """.split()
)

# Academic and lower-frequency vocabulary. A hit here is evidence of the
# precise, less common lexis band 7+ descriptors ask for.
ACADEMIC_WORDS = frozenset(
    """
    accessibility accommodate accumulate adequate advocate aggregate albeit allocate alleviate
    ambiguous analogous anomaly anticipate apparent arbitrary articulate aspect assert assess
    attain attribute augment autonomy beneficial capacity coherent coincide collapse commodity
    compatible compelling compensate complement comprehensive comprise conceive conceptual
    consequently considerable consistent constitute constrain contemporary contradict contribute
    conversely convey correlate credible criterion crucial cumulative curtail decline deduce
    deliberate demonstrate denote derive deviate differentiate diminish discrete displace
    disproportionate distinction diverse dominate dynamic elaborate eliminate emerge emphasis
    empirical enhance ensure entail equitable erode establish evident exacerbate exceed exclude
    exhibit explicit exploit extensive facilitate feasible fluctuate formulate foster fundamental
    generate hierarchy hypothesis identical illustrate impact implement implication impose
    incentive incidence inclination incorporate indicate induce inevitable infer inherent
    initiate innovation instance integral integrate intervene intrinsic invoke justify legitimate
    magnitude maintain manifest marginal mediate methodology minimise mitigate modify negligible
    nevertheless nonetheless notion notwithstanding nuanced objective obscure obtain occur offset
    ongoing outcome paradigm parallel parameter perceive persist perspective pertinent phenomenon
    plausible policy potential practitioner precede predominant preliminary presume prevalent
    principle prior prohibit prominent proportion pursue rational reciprocal refine regulate
    reinforce reluctant render represent require reside resolve respective restrain retain reveal
    rigorous scenario scope scrutiny sector sequence significant simulate simultaneous somewhat
    specify stability straightforward subordinate subsequent subsidy substantial substitute
    sufficient sustain synthesis tangible technique tension theoretical thereby threshold trace
    transition transmit trigger ultimately undergo underlying undertake uniform unprecedented
    utilise valid vary viable virtually volatile whereas widespread yield
    """.split()
)

# Cohesive devices grouped by function. Range across groups matters more for
# Coherence and Cohesion than the raw number of linkers used.
LINKER_GROUPS: dict[str, tuple[str, ...]] = {
    "addition": (
        "furthermore", "moreover", "in addition", "additionally", "besides",
        "what is more", "similarly", "likewise", "not only",
    ),
    "contrast": (
        "however", "nevertheless", "nonetheless", "on the other hand", "in contrast",
        "conversely", "whereas", "although", "though", "despite", "in spite of",
        "yet", "albeit", "while", "by contrast",
    ),
    "cause": (
        "because", "since", "therefore", "thus", "consequently", "as a result",
        "hence", "owing to", "due to", "accordingly", "so that", "for this reason",
    ),
    "example": (
        "for example", "for instance", "such as", "namely", "to illustrate",
        "in particular", "a case in point",
    ),
    "sequence": (
        "firstly", "first of all", "secondly", "thirdly", "subsequently",
        "afterwards", "initially", "to begin with", "finally",
    ),
    "conclusion": (
        "in conclusion", "to conclude", "overall", "in summary", "to sum up",
        "on balance", "all in all", "ultimately", "in short",
    ),
    "emphasis": (
        "indeed", "notably", "crucially", "above all", "in fact",
        "particularly", "significantly", "it is precisely",
    ),
    "concession": (
        "admittedly", "granted that", "it is true that", "arguably",
        "to some extent", "even if", "of course",
    ),
}

SUBORDINATORS = (
    "although", "though", "even though", "whereas", "while", "because", "since",
    "unless", "until", "whenever", "wherever", "if", "when", "after", "before",
    "so that", "in order that", "provided that", "as long as", "whether",
    "who", "whom", "whose", "which", "that",
)

COORDINATORS = ("and", "but", "or", "so", "yet", "nor", "for")

# Everyday words that a stronger essay usually replaces with something precise.
BASIC_UPGRADES: dict[str, tuple[str, ...]] = {
    "good": ("beneficial", "advantageous", "sound", "valuable"),
    "bad": ("detrimental", "harmful", "damaging", "counterproductive"),
    "big": ("substantial", "considerable", "significant", "extensive"),
    "small": ("modest", "marginal", "negligible", "limited"),
    "a lot of": ("a considerable number of", "a substantial proportion of", "numerous"),
    "lots of": ("numerous", "a great deal of", "a wide range of"),
    "very": ("particularly", "markedly", "exceptionally", "highly"),
    "really": ("genuinely", "undeniably", "distinctly"),
    "thing": ("factor", "aspect", "element", "consideration"),
    "things": ("factors", "aspects", "elements", "considerations"),
    "stuff": ("material", "content", "resources"),
    "get": ("obtain", "acquire", "secure", "achieve"),
    "give": ("provide", "supply", "grant", "afford"),
    "make": ("produce", "generate", "create", "bring about"),
    "show": ("demonstrate", "indicate", "reveal", "illustrate"),
    "help": ("assist", "facilitate", "support", "enable"),
    "use": ("employ", "utilise", "apply", "draw on"),
    "important": ("crucial", "vital", "significant", "fundamental"),
    "problem": ("issue", "challenge", "difficulty", "drawback"),
    "think": ("contend", "maintain", "argue", "hold"),
    "say": ("state", "assert", "claim", "observe"),
    "nowadays": ("in recent decades", "at present", "increasingly"),
    "many people": ("a considerable number of people", "a substantial minority", "many observers"),
    "people": ("individuals", "citizens", "the public", "society"),
    "kids": ("children", "young people", "adolescents"),
    "a bit": ("somewhat", "slightly", "to a limited extent"),
    "get better": ("improve", "advance", "progress"),
    "go up": ("rise", "increase", "climb"),
    "go down": ("fall", "decline", "decrease"),
    "find out": ("discover", "establish", "determine"),
    "look at": ("examine", "consider", "analyse"),
    "deal with": ("address", "tackle", "manage"),
    "talk about": ("discuss", "examine", "consider"),
    "come up with": ("devise", "formulate", "propose"),
    "a lot": ("considerably", "substantially", "significantly"),
    "these days": ("currently", "in the present day", "of late"),
}

# Conversational forms that weaken an academic register.
INFORMAL_MARKERS = (
    "gonna", "wanna", "gotta", "kinda", "sorta", "stuff", "kids", "guys",
    "a lot of", "lots of", "big time", "you know", "and so on", "etc",
    "nowadays", "these days", "awesome", "huge", "super", "ok", "okay",
)

# Used only when spaCy is unavailable, to spot passive constructions.
IRREGULAR_PARTICIPLES = frozenset(
    """
    been born brought built bought caught chosen done drawn driven eaten fallen felt found given
    gone grown heard held kept known laid led left lost made meant met paid put read seen sent set
    shown sold sought spent spoken taken taught thought told understood won written
    """.split()
)

REFERENCE_RE = re.compile(
    # "that" is left out: it is far more often a relativiser than a demonstrative.
    r"(?<![\w'-])(?:this|these|those|such)\s+[a-z]{4,}"
    r"|(?<![\w'-])(?:the former|the latter|the same|doing so|in doing so|to do so)(?![\w'-])",
    re.IGNORECASE,
)

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’\-]*")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])[\"'”’)\]]*\s+")
PASSIVE_RE = re.compile(
    r"\b(?:am|is|are|was|were|be|been|being)\b(?:\s+(?:\w+ly|not|never|already|also))?\s+(\w+)\b",
    re.IGNORECASE,
)


# -----------------------------------------------------------------------------
# TOKENIZATION
# -----------------------------------------------------------------------------

def _paragraphs(text: str) -> list[str]:
    blocks = [block.strip() for block in re.split(r"\n\s*\n+", text.strip()) if block.strip()]
    if blocks:
        return blocks
    single = text.strip()
    return [single] if single else []


def _sentences(text: str) -> list[str]:
    sent_tokenize = _nltk_sentence_tokenizer()
    if sent_tokenize is not None:
        try:
            found = [s.strip() for s in sent_tokenize(text) if s.strip()]
            if found:
                return found
        except Exception:
            pass
    return [s.strip() for s in SENTENCE_SPLIT_RE.split(text.strip()) if s.strip()]


def _words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def _sd(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return math.sqrt(variance)


def _phrase_hits(lowered: str, phrases: Sequence[str]) -> list[str]:
    hits: list[str] = []
    for phrase in phrases:
        if re.search(rf"(?<![\w'-]){re.escape(phrase)}(?![\w'-])", lowered):
            hits.append(phrase)
    return hits


def _phrase_count(lowered: str, phrase: str) -> int:
    return len(re.findall(rf"(?<![\w'-]){re.escape(phrase)}(?![\w'-])", lowered))


# -----------------------------------------------------------------------------
# SYNTAX ANALYSIS
# -----------------------------------------------------------------------------

_CLAUSE_DEPS = {"advcl", "relcl", "ccomp", "xcomp", "acl", "csubj", "acl:relcl"}
_PASSIVE_DEPS = {"nsubjpass", "nsubj:pass"}
_CONTENT_POS = {"NOUN", "PROPN", "VERB", "ADJ", "ADV"}


def _spacy_syntax(text: str) -> dict[str, Any] | None:
    """Dependency-based syntax counts, or ``None`` when spaCy is unavailable."""

    nlp = _spacy_nlp()
    if nlp is None:
        return None

    try:
        doc = nlp(text)
        sentences = [sent for sent in doc.sents if sent.text.strip()]
        alpha = [token for token in doc if token.is_alpha]
        content = [token for token in alpha if token.pos_ in _CONTENT_POS]

        return {
            "engine": "spacy",
            "sentence_count": len(sentences),
            "content_word_count": len(content),
            "unique_lemmas": len({token.lemma_.lower() for token in content}),
            "subordinate_clauses": sum(1 for token in doc if token.dep_ in _CLAUSE_DEPS),
            "complex_sentences": sum(
                1 for sent in sentences if any(token.dep_ in _CLAUSE_DEPS for token in sent)
            ),
            "compound_sentences": sum(
                1
                for sent in sentences
                if any(token.dep_ == "conj" and token.pos_ in {"VERB", "AUX"} for token in sent)
            ),
            "passive_count": sum(1 for token in doc if token.dep_ in _PASSIVE_DEPS),
        }
    except Exception:
        return None


def _regex_syntax(sentences: Sequence[str], words: Sequence[str]) -> dict[str, Any]:
    """Heuristic syntax counts used when spaCy is not installed."""

    complex_sentences = 0
    compound_sentences = 0
    subordinate_clauses = 0
    passive_count = 0

    for sentence in sentences:
        lowered = sentence.lower()
        found = _phrase_hits(lowered, SUBORDINATORS)
        if found:
            complex_sentences += 1
            subordinate_clauses += sum(_phrase_count(lowered, marker) for marker in found)
        if re.search(r"(,\s*(?:and|but|or|so|yet|nor)\b)|;", lowered):
            compound_sentences += 1
        for participle in PASSIVE_RE.findall(lowered):
            if participle.endswith("ed") or participle in IRREGULAR_PARTICIPLES:
                passive_count += 1

    content = [word for word in words if word.lower() not in CORE_WORDS]
    return {
        "engine": "regex",
        "sentence_count": len(sentences),
        "content_word_count": len(content),
        "unique_lemmas": len({word.lower().rstrip("s") for word in content}),
        "subordinate_clauses": subordinate_clauses,
        "complex_sentences": complex_sentences,
        "compound_sentences": compound_sentences,
        "passive_count": passive_count,
    }


# -----------------------------------------------------------------------------
# MECHANICS
# -----------------------------------------------------------------------------

def _mechanics_issues(text: str, sentences: Sequence[str]) -> list[str]:
    issues: list[str] = []

    lowercase_starts = sum(1 for s in sentences if s[:1].isalpha() and s[:1].islower())
    if lowercase_starts:
        issues.append(f"{lowercase_starts} sentence(s) do not begin with a capital letter")

    stripped = text.strip()
    if stripped and stripped[-1] not in ".!?\"'”’":
        issues.append("The text does not end with a full stop")

    if re.search(r"[^\S\n]{2,}", text):
        issues.append("Repeated spaces between words")

    if re.search(r"[,;:][A-Za-z]", text):
        issues.append("Missing space after a comma, semicolon, or colon")

    if re.search(r"\s+[,.;:!?]", text):
        issues.append("Space before a punctuation mark")

    if re.search(r"[!?]{2,}|\.{4,}", text):
        issues.append("Repeated punctuation marks")

    if re.search(r"(?<![\w'-])i(?![\w'-])", text):
        issues.append("The pronoun I is written in lower case")

    long_sentences = sum(1 for s in sentences if len(WORD_RE.findall(s)) > 45)
    if long_sentences:
        issues.append(f"{long_sentences} sentence(s) run past 45 words and are hard to follow")

    return issues


# -----------------------------------------------------------------------------
# BAND ESTIMATION
# -----------------------------------------------------------------------------

CRITERIA = ("task_response", "coherence_cohesion", "lexical_resource", "grammatical_range")

CRITERION_LABELS = {
    "task_response": "Task Response",
    "coherence_cohesion": "Coherence & Cohesion",
    "lexical_resource": "Lexical Resource",
    "grammatical_range": "Grammatical Range & Accuracy",
}


def round_half_band(value: float) -> float:
    """Clamp to the 0-9 scale and round to the nearest half band."""

    return max(0.0, min(9.0, round(float(value) * 2) / 2))


def overall_band(bands: dict[str, float]) -> float:
    """Average the four criteria the way IELTS reports an overall band."""

    scores = [float(bands.get(name, 0.0)) for name in CRITERIA]
    if not scores:
        return 0.0
    average = sum(scores) / len(scores)
    return max(0.0, min(9.0, math.floor(average * 2 + 0.5) / 2))


def _tier(value: float, steps: Sequence[tuple[float, float]]) -> float:
    for threshold, bonus in steps:
        if value >= threshold:
            return bonus
    return 0.0


def estimate_local_bands(metrics: dict[str, Any]) -> dict[str, float]:
    """Band estimates derived purely from the measurements above.

    These are the offline fallback when no model is reachable, and they are also
    sent to the model as a prior so it does not have to infer them from scratch.
    """

    sentence_count = max(1, metrics["sentence_count"])
    paragraph_count = metrics["paragraph_count"]
    paragraph_sentences = metrics["paragraph_sentence_counts"] or [0]

    lexical = 4.0
    lexical += _tier(metrics["root_type_token_ratio"], ((9, 1.5), (8, 1.2), (7, 0.9), (6, 0.6)))
    lexical += _tier(metrics["beyond_core_ratio"], ((0.45, 1.2), (0.38, 0.9), (0.30, 0.6), (0.22, 0.3)))
    lexical += _tier(metrics["academic_word_ratio"], ((0.06, 1.0), (0.04, 0.7), (0.025, 0.4), (0.012, 0.2)))
    lexical += _tier(metrics["long_word_ratio"], ((0.18, 0.5), (0.12, 0.3)))
    lexical -= min(1.0, 0.25 * len(metrics["overused_words"]))
    lexical -= min(0.6, 0.15 * len(metrics["informal_expressions"]))

    cohesion = 4.0
    cohesion += _tier(float(paragraph_count), ((4, 1.2), (3, 1.0), (2, 0.5)))
    cohesion += _tier(float(len(metrics["linker_groups_used"])), ((5, 1.2), (4, 1.0), (3, 0.7), (2, 0.4), (1, 0.2)))
    linker_density = metrics["linker_count"] / sentence_count
    if 0.25 <= linker_density <= 1.1:
        cohesion += 0.4
    if metrics["has_conclusion_signal"]:
        cohesion += 0.3
    cohesion += _tier(float(metrics["referencing_count"]), ((5, 0.6), (3, 0.4), (1, 0.2)))
    if paragraph_count >= 2 and min(paragraph_sentences) >= 2 and _sd(paragraph_sentences) <= 2.5:
        cohesion += 0.5
    if paragraph_count <= 1 and sentence_count >= 6:
        cohesion -= 0.6
    cohesion -= min(0.5, 0.25 * len(metrics["repeated_openers"]))

    grammar = 4.0
    grammar += _tier(metrics["complex_sentence_ratio"], ((0.5, 1.3), (0.35, 1.0), (0.2, 0.6), (0.01, 0.3)))
    grammar += _tier(metrics["sentence_length_sd"], ((6, 0.9), (4, 0.6), (2.5, 0.3)))
    average_length = metrics["average_sentence_length"]
    if 14 <= average_length <= 24:
        grammar += 0.6
    elif 11 <= average_length <= 28:
        grammar += 0.3
    if metrics["passive_count"] >= 1:
        grammar += 0.4
    if metrics["compound_sentence_ratio"] >= 0.15:
        grammar += 0.3
    grammar -= min(0.9, 0.2 * len(metrics["mechanics_issues"]))

    # Relevance to the prompt cannot be judged locally, so Task Response is
    # estimated from length and development only, and capped below band 8.
    task = 4.0
    length_ratio = metrics["word_count"] / max(1, metrics["min_words"])
    task += _tier(length_ratio, ((1.0, 1.5), (0.85, 1.0), (0.6, 0.4)))
    if paragraph_count >= 3:
        task += 0.6
    if metrics["has_conclusion_signal"]:
        task += 0.4
    if sum(paragraph_sentences) / max(1, paragraph_count) >= 3:
        task += 0.5

    bands = {
        "task_response": max(3.0, min(7.5, task)),
        "coherence_cohesion": max(3.0, min(8.5, cohesion)),
        "lexical_resource": max(3.0, min(8.5, lexical)),
        "grammatical_range": max(3.0, min(8.5, grammar)),
    }

    # Too little text to demonstrate range, whatever the ratios say.
    word_count = metrics["word_count"]
    if word_count < 40:
        ceiling = 4.0 if word_count < 20 else 5.0
        bands = {name: min(score, ceiling) for name, score in bands.items()}

    return {name: round_half_band(score) for name, score in bands.items()}


def apply_length_penalty(bands: dict[str, float], metrics: dict[str, Any]) -> tuple[dict[str, float], list[str]]:
    """Cap Task Response for an under-length response, as IELTS markers do.

    Deterministic and computed here so the model is never asked to arbitrate a
    rule that is purely a word count.
    """

    adjusted = dict(bands)
    notes: list[str] = []
    if metrics["meets_min_words"]:
        return adjusted, notes

    word_count = metrics["word_count"]
    minimum = metrics["min_words"]
    cap = 4.0 if word_count < minimum * 0.5 else 5.0
    notes.append(
        f"The response is {word_count} words against a {minimum}-word minimum, "
        f"so Task Response is capped at band {cap:.1f}."
    )
    if adjusted.get("task_response", 0.0) > cap:
        adjusted["task_response"] = cap
    return adjusted, notes


def build_digest(metrics: dict[str, Any]) -> str:
    """A one-line summary of the measurements, for the model prompt.

    Roughly seventy tokens, and it removes any need for the model to count.
    """

    parts = [
        f"words={metrics['word_count']} sents={metrics['sentence_count']} paras={metrics['paragraph_count']}",
        (
            f"rttr={metrics['root_type_token_ratio']:.1f}"
            f" beyond_core={metrics['beyond_core_ratio']:.2f}"
            f" academic={len(metrics['academic_words_used'])}"
            f" long={metrics['long_word_ratio']:.2f}"
        ),
        (
            f"avg_sent={metrics['average_sentence_length']:.1f}"
            f" sd={metrics['sentence_length_sd']:.1f}"
            f" complex={metrics['complex_sentence_ratio']:.2f}"
            f" compound={metrics['compound_sentence_ratio']:.2f}"
            f" passive={metrics['passive_count']}"
        ),
        "linkers=" + (",".join(metrics["linker_groups_used"]) or "none")
        + f" refs={metrics['referencing_count']}",
    ]

    if metrics["overused_words"]:
        repeated = ",".join(f"{item['word']}x{item['count']}" for item in metrics["overused_words"][:4])
        parts.append("repeated=" + repeated)
    if metrics["informal_expressions"]:
        parts.append("informal=" + ",".join(metrics["informal_expressions"][:4]))
    if metrics["mechanics_issues"]:
        parts.append(f"mechanics={len(metrics['mechanics_issues'])}")
    if not metrics["meets_min_words"]:
        parts.append(f"UNDER_LENGTH(min={metrics['min_words']})")

    return " | ".join(parts)


# -----------------------------------------------------------------------------
# PUBLIC ENTRY POINT
# -----------------------------------------------------------------------------

def analyze_writing(text: str, *, min_words: int = 250) -> dict[str, Any]:
    """Measure a piece of writing without calling any language model."""

    text = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    lowered = text.lower()

    paragraphs = _paragraphs(text)
    sentences = _sentences(text)
    words = _words(text)
    lower_words = [word.lower() for word in words]

    word_count = len(words)
    safe_words = max(1, word_count)
    sentence_count = len(sentences)
    safe_sentences = max(1, sentence_count)

    syntax = _spacy_syntax(text) if word_count else None
    if syntax is None:
        syntax = _regex_syntax(sentences, words)
    engine_sentences = max(1, syntax["sentence_count"] or sentence_count)

    unique_words = len(set(lower_words))
    beyond_core = [word for word in lower_words if word not in CORE_WORDS]
    academic_used = sorted({word for word in lower_words if word in ACADEMIC_WORDS})
    academic_count = sum(1 for word in lower_words if word in ACADEMIC_WORDS)
    long_words = sum(1 for word in lower_words if len(word) >= 8)

    sentence_lengths = [len(WORD_RE.findall(sentence)) for sentence in sentences]
    paragraph_sentence_counts = [len(_sentences(paragraph)) for paragraph in paragraphs]

    stopwords = _stopwords()
    countable = [word for word in lower_words if len(word) > 3 and word not in stopwords]
    content_counts = Counter(countable)
    overused = [
        {"word": word, "count": count}
        for word, count in content_counts.most_common(10)
        if count >= 4 or (count >= 3 and count / max(1, len(countable)) > 0.05)
    ][:6]

    opener_counts = Counter(
        " ".join(WORD_RE.findall(sentence)[:2]).lower() for sentence in sentences if sentence
    )
    repeated_openers = [
        {"opener": opener, "count": count}
        for opener, count in opener_counts.most_common(3)
        if opener and count >= 3
    ]

    linkers_by_group: dict[str, list[str]] = {}
    for group, phrases in LINKER_GROUPS.items():
        hits = _phrase_hits(lowered, phrases)
        if hits:
            linkers_by_group[group] = hits
    linker_count = sum(len(hits) for hits in linkers_by_group.values())

    final_paragraph = paragraphs[-1].lower() if paragraphs else ""
    has_conclusion_signal = bool(_phrase_hits(final_paragraph, LINKER_GROUPS["conclusion"]))

    # A single use of an everyday word is not a fault; repetition of one is.
    basic_upgrades = []
    for basic, suggestions in BASIC_UPGRADES.items():
        count = _phrase_count(lowered, basic)
        if count >= 2:
            basic_upgrades.append(
                {"basic": basic, "count": count, "suggestions": list(suggestions[:3])}
            )
    basic_upgrades.sort(key=lambda item: -item["count"])
    basic_upgrades = basic_upgrades[:8]

    metrics: dict[str, Any] = {
        "analyzer": syntax["engine"] + ("+nltk" if _nltk_sentence_tokenizer() is not None else ""),
        "min_words": min_words,
        "word_count": word_count,
        "character_count": len(text.strip()),
        "sentence_count": sentence_count,
        "paragraph_count": len(paragraphs),
        "paragraph_sentence_counts": paragraph_sentence_counts,
        "meets_min_words": word_count >= min_words,
        "words_missing": max(0, min_words - word_count),
        # Lexical resource
        "unique_words": unique_words,
        "type_token_ratio": round(unique_words / safe_words, 3),
        "root_type_token_ratio": round(unique_words / math.sqrt(safe_words), 2),
        "beyond_core_ratio": round(len(beyond_core) / safe_words, 3),
        "academic_words_used": academic_used[:20],
        "academic_word_ratio": round(academic_count / safe_words, 3),
        "long_word_ratio": round(long_words / safe_words, 3),
        "average_word_length": round(sum(len(word) for word in lower_words) / safe_words, 2),
        "lexical_density": round(syntax["content_word_count"] / safe_words, 3),
        "overused_words": overused,
        "basic_word_upgrades": basic_upgrades,
        "informal_expressions": _phrase_hits(lowered, INFORMAL_MARKERS),
        "contraction_count": len(re.findall(r"\b\w+['’](?:t|s|re|ve|ll|d|m)\b", lowered)),
        # Sentence and paragraph structure
        "average_sentence_length": round(word_count / safe_sentences, 1),
        "sentence_length_sd": round(_sd(sentence_lengths), 1),
        "shortest_sentence": min(sentence_lengths) if sentence_lengths else 0,
        "longest_sentence": max(sentence_lengths) if sentence_lengths else 0,
        "subordinate_clauses": syntax["subordinate_clauses"],
        "complex_sentence_ratio": round(syntax["complex_sentences"] / engine_sentences, 3),
        "compound_sentence_ratio": round(syntax["compound_sentences"] / engine_sentences, 3),
        "passive_count": syntax["passive_count"],
        # Cohesion
        "linkers_by_group": linkers_by_group,
        "linker_groups_used": sorted(linkers_by_group),
        "linker_count": linker_count,
        "has_conclusion_signal": has_conclusion_signal,
        "referencing_count": len(REFERENCE_RE.findall(text)),
        "repeated_openers": repeated_openers,
        # Mechanics
        "mechanics_issues": _mechanics_issues(text, sentences),
    }

    metrics["local_bands"] = estimate_local_bands(metrics)
    metrics["digest"] = build_digest(metrics)
    return metrics
