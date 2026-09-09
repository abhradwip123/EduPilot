import streamlit as st

import api_client
from state import go_to, reset_for_new_topic, PAGE_LEARNING
from components.agent_status import render_agent_workflow
from components.results import render_mastery_table, render_weak_topics


def render():

    render_agent_workflow(st.session_state.agent_stage)

    st.write("")

    st.subheader("Your Learning Profile")

    st.write("")

    # Show mastery
    render_mastery_table(
        st.session_state.mastery_scores
    )

    st.write("")

    # Show weak topics
    st.markdown("### Weak Topics")

    weak_topics = st.session_state.get(
        "weak_topics",
        []
    )

    if weak_topics:

        for topic in weak_topics:
            st.markdown(f"- {topic}")

        st.caption(
            "EduPilot identified these topics as areas that need more attention."
        )

    else:

        st.success(
            "Great job! No weak topics were identified in this assessment."
        )

    st.write("")

    # Debug information - temporarily keep this
    st.write(
        "DEBUG weak_topics:",
        st.session_state.get("weak_topics")
    )

    # Personalized learning
    if weak_topics:

        if st.button(
            "Start Personalized Learning",
            type="primary"
        ):

            try:

                with st.spinner(
                    "EduPilot is analyzing your weak topics and building a lesson..."
                ):

                    response = api_client.start_learning(
                        assessment_id=st.session_state.assessment_id,
                        student_id=st.session_state.student_id,
                    )

                # Reset only after successful API response
                reset_for_new_topic()

                st.session_state.learning_id = response["learning_id"]

                st.session_state.topic = response["topic"]

                st.session_state.mastery_score = response["mastery_score"]

                st.session_state.strategy = response["strategy"]

                st.session_state.weakness_analysis = response[
                    "weakness_analysis"
                ]

                st.session_state.lesson = response["lesson"]

                st.session_state.agent_stage = "teach"

                go_to(PAGE_LEARNING)

                st.rerun()

            except api_client.APIError as exc:

                st.error(exc.message)