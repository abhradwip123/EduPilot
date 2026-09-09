"""
state.py

Single source of truth for Streamlit session_state keys and page routing.

We deliberately do NOT use Streamlit's automatic multipage app feature
(a `pages/` folder next to app.py), because that feature auto-generates
its own sidebar navigation and runs each file as an independent script —
which fights with the state-machine style flow EduPilot needs (you can't
jump straight to "Learning Quiz" without a learning_id, etc). Instead,
navigation is controlled entirely by `st.session_state.page` inside
app.py, and the view modules live in `views/` (a plain package, not a
magic Streamlit folder).
"""

import streamlit as st

PAGE_DASHBOARD = "dashboard"
PAGE_ASSESSMENT = "assessment"
PAGE_ASSESSMENT_RESULTS = "assessment_results"
PAGE_LEARNING = "learning"
PAGE_LEARNING_QUIZ = "learning_quiz"
PAGE_ADAPTIVE_RESULT = "adaptive_result"
PAGE_TEACHER = "teacher"

DEFAULTS = {
    "page": PAGE_DASHBOARD,

    "student_id": "",
    "subject": "",
    "target_score": 70,
    "exam_date": None,
    "num_questions": 10,

    "assessment_id": None,
    "assessment_questions": [],
    "assessment_answers": {},
    "evaluation": None,

    "mastery_scores": {},
    "weak_topics": [],

    "learning_id": None,
    "topic": None,
    "strategy": None,
    "previous_strategy": None,
    "weakness_analysis": None,
    "lesson": None,
    "mastery_score": None,

    "learning_quiz_questions": [],
    "learning_quiz_answers": {},

    "previous_mastery": None,
    "new_mastery": None,
    "adaptation_attempts": 0,
    "decision": None,
    "quiz_results": None,

    "_adapted": False,
    "_next_topic_loaded": False,

    "previous_topic": None,
    "completed_topics": [],

    "learning_completed": False,
    "learning_history": [],

    "teacher_recommendation": None,

    "agent_stage": "goal",
}


def init_session_state():

    for key, value in DEFAULTS.items():

        if key not in st.session_state:

            if isinstance(value, list):
                st.session_state[key] = []

            elif isinstance(value, dict):
                st.session_state[key] = {}

            else:
                st.session_state[key] = value
        


def go_to(page: str):
    st.session_state.page = page


def reset_for_new_topic():
    """Clear everything tied to a specific learning session, so starting
    a new topic (or restarting after 'next_topic') doesn't carry over
    stale data."""
    st.session_state.learning_id = None
    st.session_state.topic = None
    st.session_state.strategy = None
    st.session_state.previous_strategy = None
    st.session_state.weakness_analysis = None
    st.session_state.lesson = None
    st.session_state.mastery_score = None
    st.session_state.learning_quiz_questions = []
    st.session_state.learning_quiz_answers = {}
    st.session_state.previous_mastery = None
    st.session_state.new_mastery = None
    st.session_state.adaptation_attempts = 0
    st.session_state.decision = None
    st.session_state.quiz_results = None
    st.session_state._adapted = False
    st.session_state._next_topic_loaded = False
    st.session_state.previous_topic = None

def reset_learning_session():

    st.session_state.assessment_id = None
    st.session_state.assessment_questions = []
    st.session_state.assessment_answers = {}
    st.session_state.evaluation = None

    st.session_state.mastery_scores = {}
    st.session_state.weak_topics = []

    st.session_state.learning_id = None
    st.session_state.topic = None
    st.session_state.strategy = None
    st.session_state.previous_strategy = None
    st.session_state.weakness_analysis = None
    st.session_state.lesson = None
    st.session_state.mastery_score = None

    st.session_state.learning_quiz_questions = []
    st.session_state.learning_quiz_answers = {}

    st.session_state.previous_mastery = None
    st.session_state.new_mastery = None
    st.session_state.adaptation_attempts = 0
    st.session_state.decision = None
    st.session_state.quiz_results = None

    st.session_state._adapted = False
    st.session_state._next_topic_loaded = False

    st.session_state.previous_topic = None
    st.session_state.completed_topics = []

    st.session_state.learning_completed = False

    st.session_state.learning_history = []

    st.session_state.teacher_recommendation = None

    st.session_state.agent_stage = "goal"


def reset_everything():
    """Full reset for demo purposes (e.g. a 'Reset Session' button)."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()
