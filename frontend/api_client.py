"""
api_client.py

Thin wrapper around the existing EduPilot FastAPI backend.

IMPORTANT:
- This file does not invent any new endpoints or fields.
- It mirrors the exact request bodies defined in backend/schemas.py
  and the exact response shapes returned by backend/routes/assessment.py
  and backend/routes/learning.py.
- /learning/quiz and /learning/adapt take `learning_id` as a plain
  function parameter (not a Pydantic body model) in your FastAPI code,
  which means FastAPI expects it as a QUERY parameter, not a JSON body.
  This client calls those two endpoints accordingly.
"""

import os
import streamlit as st
import requests


def get_api_url():

    if os.environ.get("EDUPILOT_API_URL"):
        return os.environ["EDUPILOT_API_URL"].rstrip("/")

    try:
        return st.secrets["EDUPILOT_API_URL"].rstrip("/")
    except Exception:
        return "http://127.0.0.1:8000"


API_URL = get_api_url()

TIMEOUT_SECONDS = 120


class APIError(Exception):
    """Raised for any problem talking to the backend, with a
    user-friendly message already attached."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def _handle_response(response: requests.Response):
    if not response.ok:
        detail = None
        try:
            body = response.json()
            detail = body.get("detail")
        except ValueError:
            pass

        if detail:
            raise APIError(str(detail))

        raise APIError(
            f"The backend returned an unexpected error "
            f"(status {response.status_code})."
        )

    try:
        return response.json()
    except ValueError:
        raise APIError("The backend returned a response that wasn't valid JSON.")


def _post(endpoint: str, json_body: dict | None = None, params: dict | None = None):
    url = f"{API_URL}{endpoint}"

    try:
        response = requests.post(
            url,
            json=json_body,
            params=params,
            timeout=TIMEOUT_SECONDS,
        )
    except requests.exceptions.ConnectionError:
        raise APIError(
            "Couldn't connect to the EduPilot backend. "
            f"Make sure your FastAPI server is running at {API_URL} "
            "(uvicorn backend.main:app --reload)."
        )
    except requests.exceptions.Timeout:
        raise APIError(
            "The backend took too long to respond. This can happen while "
            "the AI is generating a lesson or quiz — please try again."
        )
    except requests.exceptions.RequestException as exc:
        raise APIError(f"Request to the backend failed: {exc}")

    return _handle_response(response)


# ---------------------------------------------------------------------
# Assessment endpoints
# ---------------------------------------------------------------------

def start_assessment(student_id: str, subject: str, num_questions: int = 10) -> dict:
    """POST /assessment/start"""
    return _post(
        "/assessment/start",
        json_body={
            "student_id": student_id,
            "subject": subject,
            "num_questions": num_questions,
        },
    )


def submit_assessment(assessment_id: str, student_id: str, answers: dict) -> dict:
    """POST /assessment/submit"""
    return _post(
        "/assessment/submit",
        json_body={
            "assessment_id": assessment_id,
            "student_id": student_id,
            "answers": answers,
        },
    )


# ---------------------------------------------------------------------
# Learning endpoints
# ---------------------------------------------------------------------

def start_learning(assessment_id: str, student_id: str) -> dict:
    """POST /learning/start"""
    return _post(
        "/learning/start",
        json_body={
            "assessment_id": assessment_id,
            "student_id": student_id,
        },
    )


def get_learning_quiz(learning_id: str) -> dict:
    """POST /learning/quiz?learning_id=... (query param, per backend signature)"""
    return _post("/learning/quiz", params={"learning_id": learning_id})


def submit_learning_quiz(learning_id: str, student_id: str, answers: dict) -> dict:
    """POST /learning/quiz/submit"""
    return _post(
        "/learning/quiz/submit",
        json_body={
            "learning_id": learning_id,
            "student_id": student_id,
            "answers": answers,
        },
    )


def adapt_learning(learning_id: str) -> dict:
    """POST /learning/adapt?learning_id=... (query param, per backend signature)"""
    return _post("/learning/adapt", params={"learning_id": learning_id})

def get_teacher_insights(
    mastery_scores: dict,
    weak_topics: list,
    learning_history: list,
) -> dict:

    return _post(
        "/learning/teacher-insights",
        json_body={
            "mastery_scores": mastery_scores,
            "weak_topics": weak_topics,
            "learning_history": learning_history,
        },
    )