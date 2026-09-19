# English Practice Diagnostic

A Django app with guided English courses and three practice modes:

## English courses

Open `/courses/` or choose **Explore English courses** on the home page.

| Course | URL | Lessons |
| --- | --- | --- |
| English participles | `/courses/participles/` | Present and past forms, continuous/perfect/passive constructions, adjectives, and participle clauses |
| Write better English | `/courses/better-writing/` | Clear sentences, developed paragraphs, connections, and revision |
| Tell a better story | `/courses/storytelling/` | Character goals, plot, scenes and dialogue, and endings |
| IELTS foundations | `/courses/ielts-beginner/` | Beginner study planning, listening for details, reading for evidence, spoken answers, and short Task 1 / Task 2 drills |
| IELTS skill builder | `/courses/ielts-intermediate/` | Intermediate error review, listening decisions, reading paraphrases, Speaking Part 2, a full report, and a full essay |
| IELTS Band 8 preparation | `/courses/ielts-band-8/` | Advanced study planning, qualified claims, argument analysis, Speaking Part 3, precise reports, and nuanced essays |

The three general English courses contain four lessons each; the three IELTS paths contain six
lessons each, for **six courses and thirty lessons**. Each lesson has original explanations,
worked examples, two multiple-choice questions, a practical assignment, a review checklist,
and a sample response. Writing and storytelling
lessons build towards a final piece. Lessons can also be opened directly and revisited in any order.

**Check answers & save** stores a submitted draft and its answers in the existing Django database
session, separately from diagnostic tests. A lesson is complete after both answers are correct,
the response minimum is met, and the learner confirms the self-review. Speaking lessons also require
confirmation that the prompt was practised aloud. These completion checks do not grade the quality
or relevance of free writing. Already completed lessons remain complete
when revisited. Progress belongs to the browser session and expires with it; there is no account sync.

Draft text also autosaves on the current device using local storage when available. With JavaScript
or local storage disabled, submitting the form still saves work. Course content and exercises work
without an API key and require no additional migrations or dependencies. Edit `practice/courses.py`
to maintain general English content and `practice/ielts_courses.py` for IELTS content. Shared types
are in `practice/course_types.py`. Keep course and lesson slugs stable so saved progress still matches.

### IELTS preparation

All three IELTS paths cover listening, reading, speaking, and **Academic** Writing, with a lesson on
study planning and separate Task 1 and Task 2 lessons. Beginner writing drills are deliberately
shorter than exam tasks; intermediate and Band 8 reports require at least 150 words and essays at
least 250. Course pages link to the existing writing practice mode at the matching level.

Listening drills include original scripts, browser speech synthesis with a speed selector, and
transcripts for review. An English browser voice is required for playback. Without it or without
JavaScript, learners can ask a partner to read the transcript or follow the official IELTS audio
links. Speaking prompts include a pauseable timer, with preparation time for the long turn. The
timer uses elapsed time so background-tab throttling does not extend a turn; an ordinary clock
works as a fallback. Audio is not recorded and speaking is self-reviewed.

These are focused practice courses, not full mock tests. Completion and XP do not assess or certify
an IELTS band. Format and assessment guidance is linked to official IELTS resources in each course.

### Daily challenge and gamification

The landing page features a **word of the day** with a definition, example, and a **question of the
day** CTA. A deterministic bank of 14 original challenges rotates at **00:00 UTC**, consistently for
all visitors. The form works without JavaScript and validates both the selected option and the date
on the server. A form left open across midnight is refreshed with the current challenge instead of
awarding points for an old one. Wrong answers show feedback and can be retried.

The landing page and course pages show XP levels, current and best streaks, a seven-day activity
strip, and four unlockable badges. Rewards are:

- **40 XP** per newly completed lesson.
- **100 XP** once all lessons in a course are complete.
- **15 XP** per correctly completed daily challenge, at most once per UTC date.
- A new activity level every **200 XP**. These levels describe practice activity, not English proficiency.

New lesson completions and daily successes count towards a streak. Multiple completions on one
day count as one active day; a streak stays available through the following day and resets after a
missed day. Repeating a completed lesson does not award XP or a new streak day. Course XP is derived
from existing saved completion records, so earlier work receives credit without fabricated dates.
Badges recognise a first completion, seven consecutive days, a complete course, and practice in all
four IELTS skills.

Rewards and daily responses use the existing database-backed browser session, separate from
diagnostic test state. They survive reloads and server restarts while the session is valid, but do
not sync across browsers or accounts. Curriculum and reward changes need no migrations or API keys.
Maintain daily content in `practice/daily_challenges.py` and reward rules in `practice/gamification.py`.

## Practice modes

| Mode | URL | What it does |
| --- | --- | --- |
| Sentence | `/test/?mode=sentence` | 10 multiple-choice questions with the grammar topic hidden until you answer |
| Paragraph | `/test/?mode=paragraph` | Multi-blank cloze passages that test cohesion and paragraph flow |
| Writing | `/test/?mode=writing` | A writing task scored against the four IELTS band descriptors |

Every mode is available at five levels: `beginner`, `intermediate`, `advanced`, `ielts_8_9`, and `all`.

The question generator uses the OpenAI Python SDK pointed at OpenRouter.
If `OPENROUTER_API_KEY` is not set or the request fails, the app falls back to the local question bank so the UI still works.

## Writing mode

The learner is given a writing task and a minimum word count, writes a response, and receives an
estimated band for **Task Response**, **Coherence & Cohesion**, **Lexical Resource**, and
**Grammatical Range & Accuracy**, plus the overall band using the IELTS half-band rounding rule.

Beginner tasks are short personal writing exercises (80 words, 20 minutes), and intermediate tasks
are shorter essay practice (180 words, 30 minutes). Advanced and IELTS Band 8–9 tasks use the
[Task 2 length and timing](https://ielts.org/take-a-test/test-types/ielts-academic-test/ielts-academic-format-writing)
of at least 250 words in about 40 minutes. These are original practice prompts.

Prompts can be answered using general knowledge and experience. Vocabulary lists are optional
suggestions, and each outline illustrates one possible structure. The guidance emphasises clear
positions, developed reasons, and natural, precise language, following the
[IELTS writing assessment guidance](https://ielts.org/take-a-test/preparation-resources/writing-test-resources).

### How it keeps token use low

`practice/nlp.py` measures everything countable *before* any model is involved:

- **Lexical resource** — different words, root type-token ratio, share of vocabulary outside the
  most frequent core of English, academic word hits, over-repeated words, everyday words worth
  upgrading, informal register, contractions.
- **Sentence and paragraph structure** — paragraph count and balance, average sentence length and
  its variation, share of sentences carrying a subordinate clause, compound sentences, passive
  constructions.
- **Cohesion** — which of eight cohesive-device families appear, referencing and substitution
  (*this saving*, *such arrangements*, *the former*), whether the final paragraph signals a
  conclusion, repeated sentence openings.
- **Mechanics** — capitalisation, spacing, punctuation, over-long sentences.

Those numbers are compressed into a single digest line (about seventy tokens) that is sent with the
response. The model is told to trust it and never to recount, so it spends its tokens on judgement
alone. On top of that:

- the essay is truncated at `WRITING_MAX_ESSAY_WORDS` (default 450);
- the reply uses short JSON keys and is capped at `WRITING_MAX_OUTPUT_TOKENS` (default 700);
- the overall band and the under-length penalty are computed in Python, not paid for in tokens;
- responses under `WRITING_AI_MIN_WORDS` (default 40) are scored locally with no model call at all;
- writing prompts are never generated — they come from a fixed bank of 28 tasks.

With no API key, or when the request fails or times out, the local measurements produce the whole
report on their own, including band estimates, strengths, and specific improvements.

The local bands are an estimate, and the report labels them as such. They measure form, not meaning:
Task Response is capped below band 8 because relevance to the question cannot be judged from surface
features, and the cohesion score rewards explicit linking words, so writing that connects ideas purely
through referencing and lexical chains tends to be under-rated. Configure a model for the band that
takes content into account; the measured estimate stays visible beside it either way.

### Local analysis dependencies

NLTK provides sentence segmentation and the stopword list; spaCy adds dependency-based clause and
passive detection. Both are optional — `practice/nlp.py` probes them lazily and falls back to regex
analysis if a library or its data is missing, so the app never fails because a corpus was not
downloaded. Set `WRITING_DISABLE_SPACY=1` or `WRITING_DISABLE_NLTK=1` to force the fallback.

Words are deliberately **not** counted with NLTK. The count drives the minimum-length rule and the
Task Response cap, so it uses one fixed regular expression that produces the same number in every
deployment and matches the live counter in the browser.

To run writing mode at full fidelity outside Docker:

```bash
python -m nltk.downloader punkt punkt_tab stopwords
python -m spacy download en_core_web_sm
```

## Run locally

```bash
python3 -m pip install -r requirements.txt
export OPENROUTER_API_KEY="your_openrouter_api_key"
export OPENROUTER_MODEL="openai/gpt-4o-mini"
python manage.py migrate
python manage.py runserver 0.0.0.0:5170
```

Open `http://localhost:5170/`.

The landing page is at `/`, guided courses are at `/courses/`, and practice modes live at `/test/`.

## Tests

```bash
python manage.py test practice
```

The suite covers all three modes and never reaches the network: the writing tests either disable the
model with `WRITING_AI_ENABLED=0` or mock the evaluator.

## Run in Docker

```bash
docker build -t english-practice .
docker run --rm -p 5170:5170 \
  -e DJANGO_SECRET_KEY=change-me \
  -e DJANGO_ALLOWED_HOSTS='*' \
  -e OPENROUTER_API_KEY=your_openrouter_api_key \
  -e OPENROUTER_MODEL=openai/gpt-4o-mini \
  english-practice
```

Or use Docker Compose:

```bash
docker compose up --build
```

The app listens on port `5170` in both local and containerized runs.

The SQLite question bank is stored in `data/db.sqlite3` so Docker runs can persist generated questions across restarts when the `data/` volume is mounted. The writing prompt bank is seeded into the same database from `practice/writing_bank.py` on first use.

Corrections to writing prompt wording and supporting details are applied to existing seed entries
on use, matched by title and level. Custom entries and saved practice sessions keep their content.
Writing practice stays within the selected level; if fewer prompts are available than requested,
it returns the available unique prompts.

The active test session is stored in the same SQLite database through a Django model, so the current test can be restored after restarts as long as `data/db.sqlite3` remains in place.
