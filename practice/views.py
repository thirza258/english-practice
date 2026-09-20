from __future__ import annotations

import html
import json
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .courses import COURSES
from .daily_challenges import DAILY_ATTEMPT_KEY, challenge_for_day
from .gamification import REWARDS_KEY, learning_day, learning_summary, record_activity
from .services import (
    SUPPORTED_LEVELS,
    SUPPORTED_MODES,
    build_results,
    current_question_payload,
    initialise_session_state,
    load_state,
    normalize_level,
    normalize_mode,
    save_state,
    submit_answer,
)
from .vocabulary import DOMAIN_NAME_MAP, POS_NAME_MAP, vocabulary_repo

CANONICAL_HOST = "https://english.nevatal.id"


def robots_txt(request: HttpRequest) -> HttpResponse:
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /api/",
        "",
        f"Sitemap: {CANONICAL_HOST}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def sitemap_xml(request: HttpRequest) -> HttpResponse:
    today = timezone.now().strftime("%Y-%m-%d")

    # High-level primary routes
    entries: list[tuple[str, str, str]] = [
        (reverse("practice:landing"), "daily", "1.0"),
        (reverse("practice:courses"), "weekly", "0.9"),
        (reverse("practice:test"), "daily", "0.8"),
    ]

    # Course catalog details and lessons
    for course in COURSES:
        entries.append((reverse("practice:course-detail", args=[course.slug]), "weekly", "0.8"))
        for lesson in course.lessons:
            entries.append(
                (reverse("practice:course-lesson", args=[course.slug, lesson.slug]), "monthly", "0.7")
            )

    # Diagnostic practice test modes
    for mode in SUPPORTED_MODES:
        entries.append((f"{reverse('practice:test')}?mode={mode}", "weekly", "0.8"))
        for level in SUPPORTED_LEVELS:
            entries.append((f"{reverse('practice:test')}?mode={mode}&level={level}", "weekly", "0.7"))

    url_blocks = []
    for path, changefreq, priority in entries:
        loc = f"{CANONICAL_HOST}{path}"
        escaped_loc = html.escape(loc, quote=True)
        url_blocks.append(
            f"  <url>\n"
            f"    <loc>{escaped_loc}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>{changefreq}</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            f"  </url>"
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(url_blocks)
        + "\n</urlset>\n"
    )
    return HttpResponse(xml.strip(), content_type="application/xml; charset=utf-8")


def _error(message: str, status: int = 400, **extra: Any) -> JsonResponse:
    payload = {"ok": False, "error": message}
    payload.update(extra)
    return JsonResponse(payload, status=status)


def _load_json(request: HttpRequest) -> dict[str, Any]:
    if not request.body:
        return {}
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Request body must be valid JSON.") from exc
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object.")
    return data


def _total_items(state: dict[str, Any]) -> int:
    """How many steps the learner sees: paragraphs, writing tasks, or questions."""

    test_type = state.get("test_type") or state.get("mode") or "sentence"
    if test_type == "paragraph":
        return state.get("total_paragraphs", state["total_questions"])
    if test_type == "writing":
        return state.get("total_tasks", state["total_questions"])
    return state["total_questions"]


def _get_state_or_error(request: HttpRequest, test_id: str) -> tuple[dict[str, Any] | None, JsonResponse | None]:
    state = load_state(request)
    if not state:
        return None, _error("No active test session was found.", status=404)
    if state.get("id") != test_id:
        return None, _error("The requested test session does not match the active session.", status=404)
    return state, None


def _landing_context(request: HttpRequest, today=None):
    today = today or learning_day()
    challenge = challenge_for_day(today)
    attempt = request.session.get(DAILY_ATTEMPT_KEY, {})
    checked = attempt.get("date") == today.isoformat()
    solved = today.isoformat() in request.session.get(REWARDS_KEY, {}).get("daily_solved", [])
    return {
        "canonical_url": f"{CANONICAL_HOST}{reverse('practice:landing')}",
        "ielts_courses": [course for course in COURSES if course.is_ielts],
        "learning": learning_summary(request.session, today=today),
        "daily": challenge,
        "daily_date": today,
        "daily_checked": checked,
        "daily_solved": solved,
        "daily_selected": attempt.get("answer") if checked else None,
        "daily_options": list(enumerate(challenge.question.options)),
    }


@require_GET
def landing(request: HttpRequest):
    return render(
        request,
        "practice/landing.html",
        _landing_context(request),
    )


@require_POST
def daily_challenge(request: HttpRequest):
    today = learning_day()
    challenge = challenge_for_day(today)
    error = None
    if request.POST.get("date") != today.isoformat():
        error = "A new daily challenge is ready. Try the current question below."
    elif request.POST.get("answer") not in {str(i) for i in range(len(challenge.question.options))}:
        error = "Choose one of the answers before checking today's question."
    if error:
        return render(request, "practice/landing.html", {
            **_landing_context(request, today), "daily_error": error,
        }, status=400)

    already_solved = today.isoformat() in request.session.get(REWARDS_KEY, {}).get("daily_solved", [])
    if not already_solved:
        answer = int(request.POST["answer"])
        request.session[DAILY_ATTEMPT_KEY] = {"date": today.isoformat(), "answer": answer}
        if answer == challenge.question.correct:
            record_activity(request.session, daily=True, today=today)
    return redirect(f"{reverse('practice:landing')}#daily-challenge")


def test_page(request: HttpRequest):
    state = load_state(request)
    requested_level = request.GET.get("level")
    requested_mode = request.GET.get("mode")

    if requested_level:
        requested_level = normalize_level(requested_level)
    if requested_mode:
        requested_mode = normalize_mode(requested_mode)

    # If user explicitly navigated with a ?level or ?mode param that differs from state, reset state
    if state:
        state_level = state.get("level")
        state_mode = state.get("test_type") or state.get("mode")
        if (requested_level and state_level != requested_level) or (requested_mode and state_mode != requested_mode):
            state = None

    initial_results = build_results(state) if state and state.get("completed") else None
    active_mode = requested_mode or (state.get("test_type") if state else "sentence")
    active_level = requested_level or (state.get("level") if state else "all")

    return render(
        request,
        "practice/test.html",
        {
            "canonical_url": f"{CANONICAL_HOST}{reverse('practice:test')}",
            "initial_state": state,
            "initial_results": initial_results,
            "requested_level": active_level,
            "requested_mode": active_mode,
        },
    )


@csrf_exempt
@require_POST
def start_test(request: HttpRequest):
    level = "all"
    mode = "sentence"
    try:
        data = _load_json(request)
        level = data.get("level") or request.GET.get("level") or "all"
        mode = data.get("mode") or data.get("test_type") or request.GET.get("mode") or "sentence"
    except ValueError:
        pass

    try:
        state = initialise_session_state(level=level, mode=mode)
    except ValueError as exc:
        return _error(f"Could not prepare the test: {exc}", status=503)
    save_state(request, state)
    total_items = _total_items(state)
    return JsonResponse(
        {
            "ok": True,
            "test_id": state["id"],
            "test_type": state.get("test_type", "sentence"),
            "mode": state.get("test_type", "sentence"),
            "level": state.get("level", "all"),
            "total_questions": state["total_questions"],
            "total_items": total_items,
            "score": state["score"],
            "progress": {"current": 1, "total": total_items},
            "question": current_question_payload(state),
        }
    )


@csrf_exempt
@require_POST
def retry_test(request: HttpRequest, test_id: str):
    level = None
    mode = None
    try:
        data = _load_json(request)
        level = data.get("level") or request.GET.get("level")
        mode = data.get("mode") or data.get("test_type") or request.GET.get("mode")
    except ValueError:
        pass

    existing_state = load_state(request)
    if not level and existing_state:
        level = existing_state.get("level", "all")
    if not mode and existing_state:
        mode = existing_state.get("test_type") or existing_state.get("mode") or "sentence"

    try:
        new_state = initialise_session_state(level=level or "all", mode=mode or "sentence")
    except ValueError as exc:
        return _error(f"Could not prepare the test: {exc}", status=503)
    save_state(request, new_state)
    total_items = _total_items(new_state)
    return JsonResponse(
        {
            "ok": True,
            "test_id": new_state["id"],
            "test_type": new_state.get("test_type", "sentence"),
            "mode": new_state.get("test_type", "sentence"),
            "level": new_state.get("level", "all"),
            "total_questions": new_state["total_questions"],
            "total_items": total_items,
            "score": new_state["score"],
            "progress": {"current": 1, "total": total_items},
            "question": current_question_payload(new_state),
        }
    )


@csrf_exempt
@require_POST
def answer_test(request: HttpRequest, test_id: str):
    state, error = _get_state_or_error(request, test_id)
    if error:
        return error

    try:
        data = _load_json(request)
        test_type = state.get("test_type") or state.get("mode") or "sentence"
        if test_type == "writing":
            essay = data.get("essay")
            if not isinstance(essay, str):
                essay = data.get("text") or data.get("response") or ""
            result = submit_answer(state, str(essay))
        elif test_type == "paragraph":
            answers_payload = data.get("answers") or data.get("selected_answers") or {}
            result = submit_answer(state, answers_payload)
        else:
            selected_answer = str(data.get("selected_answer", "")).strip().upper()
            result = submit_answer(state, selected_answer)
    except ValueError as exc:
        return _error(str(exc))

    save_state(request, state)
    payload = {
        "ok": True,
        "test_id": state["id"],
        "test_type": state.get("test_type", "sentence"),
        "mode": state.get("test_type", "sentence"),
        "level": state.get("level", "all"),
        **result,
    }
    if state["completed"]:
        payload["results"] = build_results(state)
    return JsonResponse(payload)


@require_GET
def test_results(request: HttpRequest, test_id: str):
    state, error = _get_state_or_error(request, test_id)
    if error:
        return error
    if not state["completed"]:
        return _error("The test is not complete yet.", status=409)
    return JsonResponse({"ok": True, **build_results(state)})


@require_GET
def vocabulary_sample(request: HttpRequest) -> JsonResponse:
    """Return authentic vocabulary sample and context from Oxford 5000 and AVL datasets."""
    level = request.GET.get("level", "all")
    mode = request.GET.get("mode", "sentence")
    try:
        count = int(request.GET.get("count", 8))
    except ValueError:
        count = 8

    context_prompt = vocabulary_repo.format_prompt_vocabulary_context(level=level, count=count, mode=mode)
    oxford_sample = [
        {"word": w.word, "pos": w.pos, "level": w.level}
        for w in vocabulary_repo.get_oxford_sample(level=level, count=count)
    ]
    academic_sample = [
        {
            "family": fam.family,
            "fam_rank": fam.fam_rank,
            "fam_freq": fam.fam_freq,
            "words": [
                {
                    "word": e.word,
                    "pos": POS_NAME_MAP.get(e.pos, e.pos),
                    "freq": e.freq,
                    "categ": "core academic" if e.categ == "y" else "technical domain" if e.categ == "r" else "general member",
                    "domain": DOMAIN_NAME_MAP.get(e.domain, e.domain) if e.domain else "General Academic",
                }
                for e in fam.words[:6]
            ],
        }
        for fam in vocabulary_repo.get_academic_sample(level=level, count=max(4, count // 2))
    ]

    return JsonResponse(
        {
            "ok": True,
            "level": level,
            "mode": mode,
            "context_prompt": context_prompt,
            "oxford_words": oxford_sample,
            "academic_families": academic_sample,
        }
    )


@require_GET
def vocabulary_lookup(request: HttpRequest) -> JsonResponse:
    """Look up a word in Oxford 5000 and AVL datasets."""
    query = request.GET.get("q", "").strip()
    if not query:
        return _error("Query parameter 'q' is required.")
    data = vocabulary_repo.lookup_word(query)
    return JsonResponse({"ok": True, **data})
