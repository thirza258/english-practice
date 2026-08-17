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
    initial_results = build_results(state) if state and state.get("completed") else None
    return render(
        request,
        "practice/test.html",
        {
            "canonical_url": request.build_absolute_uri(reverse("practice:test")),
            "initial_state": state,
            "initial_results": initial_results,
        },
    )


@csrf_exempt
@require_POST
def start_test(request: HttpRequest):
    state = initialise_session_state()
    save_state(request, state)
    return JsonResponse(
        {
            "ok": True,
            "test_id": state["id"],
            "total_questions": state["total_questions"],
            "score": state["score"],
            "progress": {"current": 1, "total": state["total_questions"]},
            "question": current_question_payload(state),
        }
    )


@csrf_exempt
@require_POST
def retry_test(request: HttpRequest, _test_id: str):
    new_state = initialise_session_state()
    save_state(request, new_state)
    return JsonResponse(
        {
            "ok": True,
            "test_id": new_state["id"],
            "total_questions": new_state["total_questions"],
            "score": new_state["score"],
            "progress": {"current": 1, "total": new_state["total_questions"]},
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
        selected_answer = str(data.get("selected_answer", "")).strip().upper()
        result = submit_answer(state, selected_answer)
    except ValueError as exc:
        return _error(str(exc))

    save_state(request, state)
    payload = {
        "ok": True,
        "test_id": state["id"],
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
