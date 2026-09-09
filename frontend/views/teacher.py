import streamlit as st
import api_client

from components.agent_status import render_agent_workflow
from state import go_to, PAGE_DASHBOARD


def render():

    render_agent_workflow(
        st.session_state.agent_stage
    )

    st.write("")

    st.subheader("Teacher Insights")

    st.caption(
        "Instructor view: student mastery, adaptive learning history, "
        "priority topics, and AI-generated recommendations."
    )

    st.write("")

    # =========================================================
    # GET SESSION DATA
    # =========================================================

    mastery_scores = st.session_state.get(
        "mastery_scores",
        {}
    )

    weak_topics = st.session_state.get(
        "weak_topics",
        []
    )

    learning_history = st.session_state.get(
        "learning_history",
        []
    )

    completed_topics = st.session_state.get(
        "completed_topics",
        []
    )

    # =========================================================
    # NO DATA
    # =========================================================

    if not mastery_scores:

        st.info(
            "No student performance data is available yet. "
            "Complete a diagnostic assessment first."
        )

        if st.button(
            "Back to Dashboard",
            type="primary"
        ):
            go_to(PAGE_DASHBOARD)
            st.rerun()

        return

    # =========================================================
    # OVERALL STATUS
    # =========================================================

    overall_mastery = (
        sum(mastery_scores.values())
        / len(mastery_scores)
    )

    if overall_mastery >= 80:

        status = "Strong"

    elif overall_mastery >= 70:

        status = "On Track"

    else:

        status = "Needs Support"

    # =========================================================
    # STUDENT OVERVIEW
    # =========================================================

    st.markdown("### Student Overview")

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Overall Mastery",
            f"{overall_mastery:.0f}%"
        )

    with col2:

        st.metric(
            "Topics",
            len(mastery_scores)
        )

    with col3:

        st.metric(
            "Status",
            status
        )

    st.write("")

    st.write("---")

    # =========================================================
    # TOPIC PERFORMANCE
    # =========================================================

    st.markdown("### Topic Performance")

    st.write("")

    sorted_topics = sorted(
        mastery_scores.items(),
        key=lambda item: item[1]
    )

    for topic, score in sorted_topics:

        st.write(
            f"**{topic}** — {score:.0f}%"
        )

        st.progress(
            min(
                max(score / 100, 0.0),
                1.0
            )
        )

        if score < 50:

            st.error(
                "High priority support required."
            )

        elif score < 70:

            st.warning(
                "Needs additional practice."
            )

        else:

            st.success(
                "Topic mastered."
            )

        st.write("")

    st.write("---")

    # =========================================================
    # TOPICS REQUIRING ATTENTION
    # =========================================================

    st.markdown("### Topics Requiring Attention")

    st.write("")

    if weak_topics:

        for topic in weak_topics:

            score = mastery_scores.get(
                topic,
                0
            )

            st.warning(
                f"{topic}: {score:.0f}% mastery"
            )

    else:

        st.success(
            "No weak topics currently identified."
        )

    st.write("---")

    # =========================================================
    # ADAPTIVE LEARNING ANALYSIS
    # =========================================================

    st.markdown("### Adaptive Learning Analysis")

    st.write("")

    if learning_history:

        topic_events = {}

        for entry in learning_history:

            topic = entry.get(
                "topic",
                "Unknown"
            )

            topic_events[topic] = (
                topic_events.get(topic, 0) + 1
            )

        for topic, events in topic_events.items():

            if events >= 3:

                st.warning(
                    f"{topic}: {events} learning cycles recorded. "
                    "Consider teacher intervention."
                )

            elif events == 2:

                st.info(
                    f"{topic}: 2 learning cycles recorded. "
                    "Monitor progress closely."
                )

            else:

                st.write(
                    f"**{topic}**: "
                    f"{events} learning cycle recorded."
                )

    else:

        st.info(
            "Adaptive learning history will appear "
            "after the student completes a learning quiz."
        )

    st.write("---")

    # =========================================================
    # ADAPTIVE LEARNING HISTORY
    # =========================================================

    st.markdown("### Adaptive Learning History")

    st.write("")

    if learning_history:

        for index, entry in enumerate(
            learning_history,
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
                f"**Step {index} — {topic}**"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.write(
                    f"Mastery: {previous}% → {new}%"
                )

            with col2:

                st.write(
                    "Strategy: "
                    f"{strategy.replace('_', ' ').title()}"
                )

            with col3:

                st.write(
                    f"Learning adaptation event: {attempt}"
                )

            st.write("")

    else:

        st.info(
            "No adaptive learning history is available yet."
        )

    st.write("---")

    # =========================================================
    # SESSION SUMMARY
    # =========================================================

    st.markdown("### Session Summary")

    st.write("")

    learning_completed = st.session_state.get(
        "learning_completed",
        False
    )

    total_learning_events = len(
        learning_history
    )

    st.write(
        f"**Adaptive learning cycles:** "
        f"{total_learning_events}"
    )

    st.write(
        f"**Completed topics:** "
        f"{len(completed_topics)} / {len(mastery_scores)}"
    )

    if learning_completed:

        st.success(
            "The adaptive learning path has been completed."
        )

    else:

        st.info(
            "The adaptive learning path is still in progress."
        )

    st.write("---")

    # =========================================================
    # AI TEACHER RECOMMENDATION
    # =========================================================

    st.markdown("### AI Teacher Recommendation")

    st.caption(
        "Generated from the student's current mastery "
        "and adaptive learning history."
    )

    st.write("")

    if "teacher_recommendation" not in st.session_state:

        st.session_state.teacher_recommendation = None

    if st.button(
        "Generate AI Recommendation",
        type="primary"
    ):

        try:

            with st.spinner(
                "EduPilot is analyzing the student's learning data..."
            ):

                response = api_client.get_teacher_insights(

                    mastery_scores=mastery_scores,

                    weak_topics=weak_topics,

                    learning_history=learning_history,
                )

            st.session_state.teacher_recommendation = (
                response.get(
                    "recommendation",
                    "No recommendation was generated."
                )
            )

        except api_client.APIError as exc:

            st.error(
                exc.message
            )
        except Exception as exc:

            st.error(
                "The AI recommendation could not be generated "
                "at the moment."
            )

    if st.session_state.teacher_recommendation:

        st.markdown(
            st.session_state.teacher_recommendation
        )

    st.write("---")

    # =========================================================
    # BACK TO DASHBOARD
    # =========================================================

    if st.button(
        "Back to Dashboard",
        type="primary"
    ):

        go_to(PAGE_DASHBOARD)

        st.rerun()