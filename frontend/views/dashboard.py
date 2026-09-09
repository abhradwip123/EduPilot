import streamlit as st
import api_client

from state import (
    go_to,
    PAGE_DASHBOARD,
    PAGE_ASSESSMENT,
    PAGE_TEACHER,
    reset_learning_session,
)

from components.agent_status import render_agent_workflow
from components.results import (
    render_mastery_table,
    render_weak_topics,
)


def render():

    render_agent_workflow(
        st.session_state.agent_stage
    )

    st.write("")

    st.subheader("Dashboard")

    st.write("")

    # =========================================================
    # CALCULATE PROGRESS
    # =========================================================
    mastery_scores = (
        st.session_state.mastery_scores or {}
    )

    weak_topics = (
        st.session_state.weak_topics or []
    )

    total_topics = len(
        mastery_scores
    )

    # ---------------------------------------------------------
    # Determine completed topics from current mastery
    # ---------------------------------------------------------

    completed_count = sum(
        1
        for score in mastery_scores.values()
        if score >= 70
    )

    # ---------------------------------------------------------
    # Determine remaining weak topics
    # ---------------------------------------------------------

    remaining_weak_topics = sum(
        1
        for score in mastery_scores.values()
        if score < 70
    )

    # ---------------------------------------------------------
    # Calculate overall mastery
    # ---------------------------------------------------------

    if mastery_scores:

        overall_mastery = (
            sum(mastery_scores.values())
            / len(mastery_scores)
        )

    else:

        overall_mastery = 0

    # =========================================================
    # TOP PROGRESS METRICS
    # =========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Overall Mastery",
            f"{overall_mastery:.0f}%"
        )

    with col2:

        st.metric(
            "Topics Completed",
            f"{completed_count} / {total_topics}"
        )

    with col3:

        st.metric(
            "Weak Topics Remaining",
            remaining_weak_topics
        )

    with col4:

        st.metric(
            "Adaptation Attempts",
            st.session_state.adaptation_attempts
        )

    st.write("")

    # =========================================================
    # LEARNING PROGRESS
    # =========================================================

    if mastery_scores:

        st.markdown("### Learning Progress")

        st.write("")

        for topic, score in mastery_scores.items():

            st.write(
                f"**{topic}** — {score:.0f}%"
            )

            st.progress(
                min(max(score / 100, 0.0), 1.0)
            )

            st.write("")

    # =========================================================
    # MASTERY TABLE
    # =========================================================

    if mastery_scores:

        st.markdown("### Mastery Overview")

        render_mastery_table(
            mastery_scores
        )

        st.write("")

        render_weak_topics(
            weak_topics
        )

    else:

        st.info(
            "Take the diagnostic assessment to see "
            "your learning profile."
        )

    st.write("---")

    # =========================================================
    # ADAPTIVE AGENT STATUS
    # =========================================================

    st.markdown("### Adaptive Learning Status")

    if st.session_state.get("learning_completed", False):

        st.success(
            "Adaptive learning path completed."
        )

        mastered_count = sum(
            1
            for score in mastery_scores.values()
            if score >= 70
        )

        st.write(
            f"Topics mastered: {mastered_count}"
        )

    elif st.session_state.learning_id:

        st.write(
            f"**Current topic:** "
            f"{st.session_state.topic or 'Not selected'}"
        )

        st.write(
            f"**Current mastery:** "
            f"{st.session_state.mastery_score or 0}%"
        )

        st.write(
            f"**Current strategy:** "
            f"{st.session_state.strategy or 'Not selected'}"
        )

        if st.session_state.weakness_analysis:

            with st.expander(
                "View current weakness analysis"
            ):

                st.write(
                    st.session_state.weakness_analysis
                )

    else:

        st.write(
            "No adaptive learning session has been started yet."
        )
    # =========================================================
    # LEARNING OUTCOME
    # =========================================================

    if st.session_state.get("learning_completed", False):

        st.markdown("### Learning Outcome")

        st.success(
            "The student has completed the adaptive learning path "
            "and mastered all identified weak topics."
        )

    elif st.session_state.learning_id:

        st.markdown("### Learning Outcome")

        st.info(
            "The student is currently progressing through "
            "the adaptive learning path."
        )

    # =========================================================
    # LEARNING SESSION HISTORY
    # =========================================================

    learning_history = st.session_state.get(
        "learning_history",
        []
    )

    if learning_history:

        st.markdown("### Learning Session History")

        st.write("")

        for index, entry in enumerate(
            reversed(learning_history),
            start=1
        ):

            topic = entry.get(
                "topic",
                "Unknown"
            )

            previous = entry.get(
                "previous_mastery",
                0
            )

            new = entry.get(
                "new_mastery",
                0
            )

            strategy = entry.get(
                "strategy",
                "Unknown"
            )

            attempt = entry.get(
                "adaptation_attempt",
                0
            )

            st.markdown(
                f"**{topic}**"
            )

            st.write(
                f"Mastery: {previous}% → {new}%"
            )

            st.write(
                f"Strategy: "
                f"{strategy.replace('_', ' ').title()}"
            )

            st.write(
                f"Adaptation attempt: {attempt}"
            )

            if index < len(learning_history):

                st.write("---")
    

    st.write("")
    st.write("---")

    # TEACHER INSIGHTS
    if st.button(
        "Open Teacher Insights",
        type="secondary"
    ):
        

        go_to(PAGE_TEACHER)
        st.rerun()

    st.write("---")

    if st.button(
        "Start New Learning Session",
        type="secondary"
    ):
        reset_learning_session()
        go_to(PAGE_DASHBOARD)
        st.rerun()


    # =========================================================
    # START ASSESSMENT
    # =========================================================

    ready_to_start = bool(
        st.session_state.student_id
        and st.session_state.subject
    )

    if not ready_to_start:

        st.warning(
            "Enter your Student ID and Subject "
            "in the sidebar to begin."
        )

    if st.button(
        "Start Diagnostic Assessment",
        type="primary",
        disabled=not ready_to_start
    ):
        reset_learning_session()

        try:

            with st.spinner(
                "Preparing your diagnostic assessment..."
            ):

                response = api_client.start_assessment(

                    student_id=(
                        st.session_state.student_id
                    ),

                    subject=(
                        st.session_state.subject
                    ),

                    num_questions=(
                        st.session_state.num_questions
                    ),
                )
                
            questions = response.get(
                "questions"
            ) or []

            if not questions:

                st.error(
                    f"No diagnostic questions were found "
                    f"for subject "
                    f"'{st.session_state.subject}'. "
                    f"Try a different subject."
                )

                return

            st.session_state.assessment_id = (
                response["assessment_id"]
            )


            st.session_state.assessment_questions = (
                questions
            )

            st.session_state.assessment_answers = {}

            st.session_state.agent_stage = "assess"

            go_to(PAGE_ASSESSMENT)

            st.rerun()

        except api_client.APIError as exc:

            st.error(
                exc.message
            )
