import streamlit as st

import api_client
from state import go_to, PAGE_ASSESSMENT_RESULTS
from components.agent_status import render_agent_workflow
from components.progress import render_progress
from components.quiz import render_questions, all_answered


def render():
    render_agent_workflow(st.session_state.agent_stage)
    st.write("")

    st.subheader("Diagnostic Assessment")
    st.write("Let's understand your current knowledge before creating your learning plan.")
    st.write("")

    questions = st.session_state.assessment_questions

    if not questions:
        st.error("No assessment questions available. Please restart from the dashboard.")
        return

    answers = render_questions(questions, key_prefix="diag")
    st.session_state.assessment_answers = answers

    render_progress(len(answers), len(questions))

    ready = all_answered(questions, answers)
    if not ready:
        st.caption("Please answer all questions before submitting.")

    if st.button("Submit Assessment", type="primary", disabled=not ready):
        try:
            with st.spinner("Evaluating your answers..."):
                response = api_client.submit_assessment(
                    assessment_id=st.session_state.assessment_id,
                    student_id=st.session_state.student_id,
                    answers=answers,
                )

            st.session_state.evaluation = response.get("evaluation")
            st.session_state.mastery_scores = response.get("mastery_scores", {})
            st.session_state.weak_topics = response.get("weak_topics", [])
            st.session_state.agent_stage = "analyze"
            go_to(PAGE_ASSESSMENT_RESULTS)
            st.rerun()

        except api_client.APIError as exc:
            st.error(exc.message)