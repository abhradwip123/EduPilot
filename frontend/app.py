import streamlit as st

import requests
from state import (
    PAGE_TEACHER,
    init_session_state,
    PAGE_DASHBOARD,
    PAGE_ASSESSMENT,
    PAGE_ASSESSMENT_RESULTS,
    PAGE_LEARNING,
    PAGE_LEARNING_QUIZ,
    PAGE_ADAPTIVE_RESULT,
)

from components.header import render_header
from components.sidebar import render_sidebar

from views import (
    dashboard,
    assessment,
    assessment_results,
    learning,
    learning_quiz,
    adaptive_result,
    teacher,
)


st.set_page_config(
    page_title="EduPilot",
    layout="wide",
)


# --------------------------------------------------
# Global styling
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* Main application */
    .stApp {
        background-color: #FFFFFF;
    }

    /* Metric values */
    [data-testid="stMetricValue"] {
        color: #1D4ED8;
    }

    /* Primary buttons */
    button[kind="primary"] {
        background-color: #2563EB !important;
        border: 1px solid #2563EB !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    button[kind="primary"]:hover {
        background-color: #1D4ED8 !important;
        border-color: #1D4ED8 !important;
        color: #FFFFFF !important;
    }

    button[kind="primary"]:disabled {
        background-color: #CBD5E1 !important;
        border-color: #CBD5E1 !important;
        color: #64748B !important;
    }

    /* Normal buttons */
    .stButton > button {
        font-weight: 500;
        border-radius: 6px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
    }

    /* Remove unnecessary top spacing */
    .block-container {
        padding-top: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Initialize application state
# --------------------------------------------------

init_session_state()

import api_client

st.sidebar.write(
    "Backend URL:"
)

st.sidebar.code(
    api_client.API_URL
)

try:
    test_response = requests.get(
        f"{api_client.API_URL}/",
        timeout=30,
    )

    st.sidebar.write(
        f"Backend test status: {test_response.status_code}"
    )

except Exception as exc:

    st.sidebar.error(
        f"Backend test failed: {exc}"
    )


# --------------------------------------------------
# Render common components
# --------------------------------------------------

render_header()
render_sidebar()


# --------------------------------------------------
# Page routing
# --------------------------------------------------

PAGE_RENDERERS = {

    PAGE_DASHBOARD:
        dashboard.render,

    PAGE_ASSESSMENT:
        assessment.render,

    PAGE_ASSESSMENT_RESULTS:
        assessment_results.render,

    PAGE_LEARNING:
        learning.render,

    PAGE_LEARNING_QUIZ:
        learning_quiz.render,

    PAGE_ADAPTIVE_RESULT:
        adaptive_result.render,

    PAGE_TEACHER: 
        teacher.render,
}


current_page = st.session_state.get(
    "page",
    PAGE_DASHBOARD
)


renderer = PAGE_RENDERERS.get(
    current_page,
    dashboard.render
)


renderer()