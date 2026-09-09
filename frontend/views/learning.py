import streamlit as st
import time
import api_client
from state import go_to, PAGE_LEARNING_QUIZ
from components.agent_status import render_agent_workflow


STRATEGY_LABELS = {
    "concept_explanation": "Conceptual Explanation",
    "worked_examples": "Worked Examples",
    "practice_questions": "Practice Questions",
    "real_world_examples": "Real World Examples",
}


def _label(strategy):
    if not strategy:
        return "—"
    return STRATEGY_LABELS.get(strategy, strategy.replace("_", " ").title())


def render():
    render_agent_workflow(st.session_state.agent_stage)
    st.write("")

    st.subheader("Your Personalized Learning Plan")
    st.write("")

    st.markdown("**Priority 1**")
    st.markdown(f"### {st.session_state.topic}")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Mastery", f"{st.session_state.mastery_score}%")
    with col2:
        st.metric("Strategy", _label(st.session_state.strategy))

    with st.expander("Why this topic and strategy?"):
        st.write(st.session_state.weakness_analysis or "No analysis available.")

    st.write("---")
    st.markdown("### Lesson")

    if st.session_state.lesson:
        st.markdown(st.session_state.lesson)
    else:
        st.info("No lesson content was returned by the backend.")

    st.write("")

    if st.button("Check Your Understanding (Take Quiz)", type="primary"):
        try:
            with st.spinner("EduPilot is generating your quiz..."):
                response = api_client.get_learning_quiz(st.session_state.learning_id)

            questions = response.get("questions") or []
            if not questions:
                st.error("EduPilot couldn't generate quiz questions. Please try again.")
                return

            st.session_state.learning_quiz_questions = questions
            st.session_state.learning_quiz_answers = {}
            st.session_state.agent_stage = "quiz"
            go_to(PAGE_LEARNING_QUIZ)
            st.rerun()

        except api_client.APIError as exc:
            st.error(exc.message)