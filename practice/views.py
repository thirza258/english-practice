from __future__ import annotations

import json
from typing import Any

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .services import (
    build_results,
    current_question_payload,
    initialise_session_state,
    load_state,
    normalize_level,
    normalize_mode,
    save_state,
    submit_answer,
)


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


def _get_state_or_error(request: HttpRequest, test_id: str) -> tuple[dict[str, Any] | None, JsonResponse | None]:
    state = load_state(request)
    if not state:
        return None, _error("No active test session was found.", status=404)
    if state.get("id") != test_id:
        return None, _error("The requested test session does not match the active session.", status=404)
    return state, None


def landing(request: HttpRequest):
    return render(
        request,
        "practice/landing.html",
        {
            "canonical_url": request.build_absolute_uri(reverse("practice:landing")),
        },
    )


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
            "canonical_url": request.build_absolute_uri(reverse("practice:test")),
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

    state = initialise_session_state(level=level, mode=mode)
    save_state(request, state)
    total_items = state.get("total_paragraphs") if state.get("test_type") == "paragraph" else state["total_questions"]
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

    new_state = initialise_session_state(level=level or "all", mode=mode or "sentence")
    save_state(request, new_state)
    total_items = new_state.get("total_paragraphs") if new_state.get("test_type") == "paragraph" else new_state["total_questions"]
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
        if test_type == "paragraph":
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
