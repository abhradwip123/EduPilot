import streamlit as st
import api_client

from state import (
    go_to,
    reset_for_new_topic,
    PAGE_DASHBOARD,
    PAGE_LEARNING,
)

from components.agent_status import render_agent_workflow


ACTION_LABELS = {
    "teach_again": "Teach Again",
    "next_topic": "Move to Next Topic",
    "human_intervention": "Recommend Teacher Review",
}


STRATEGY_LABELS = {
    "concept_explanation": "Conceptual Explanation",
    "worked_examples": "Worked Examples",
    "practice_questions": "Practice Questions",
    "advanced_practice": "Advanced Practice",
}


def _strategy_label(strategy):
    if not strategy:
        return "—"

    return STRATEGY_LABELS.get(
        strategy,
        strategy.replace("_", " ").title()
    )


def render():

    render_agent_workflow(st.session_state.agent_stage)

    st.write("")

    st.subheader("EduPilot analyzed your performance")

    st.write("")

    # ---------------------------------------------------------
    # MASTERY SUMMARY
    # ---------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Previous Mastery",
            f"{st.session_state.previous_mastery}%"
        )

    with col2:
        st.metric(
            "New Mastery",
            f"{st.session_state.new_mastery}%"
        )

    st.write(
        f"**Adaptation attempt:** "
        f"{st.session_state.adaptation_attempts}"
    )

    decision = st.session_state.decision or {}

    action = decision.get("action")

    st.write(
        f"**Agent decision:** "
        f"{ACTION_LABELS.get(action, action or 'Unknown')}"
    )

    if decision.get("reason"):
        st.caption(decision["reason"])

    st.write("---")
    # =========================================================
    # QUIZ FEEDBACK
    # =========================================================

    quiz_results = st.session_state.get(
        "quiz_results"
    )

    if quiz_results:

        st.markdown("### Quiz Feedback")

        question_results = quiz_results.get(
            "question_results",
            []
        )

        if question_results:

            correct_count = sum(
                1
                for result in question_results
                if result.get("correct")
            )

            total_questions = len(
                question_results
            )

            st.write(
                f"**Score:** "
                f"{correct_count} / {total_questions}"
            )

            st.write("")

            for position, result in enumerate(
                question_results,
                start=1
            ):

                if result.get("correct"):

                    st.success(
                        f"Question {position}: Correct"
                    )

                else:

                    st.error(
                        f"Question {position}: Incorrect"
                    )

                    st.write(
                        f"Your answer: "
                        f"{result.get('student_answer', 'Not answered')}"
                    )

                    st.write(
                        f"Correct answer: "
                        f"{result.get('correct_answer', 'Not available')}"
                    )

                st.write("")

    # =========================================================
    # NEXT TOPIC
    # =========================================================

    if action == "next_topic":

        # -----------------------------------------------------
        # Load the next weak topic only once
        # -----------------------------------------------------

        if not st.session_state.get("_next_topic_loaded", False):

            try:

                with st.spinner(
                    "EduPilot mastered this topic and is selecting "
                    "the next weak topic..."
                ):

                    response = api_client.adapt_learning(
                        st.session_state.learning_id
                    )

                # -------------------------------------------------
                # No weak topics remaining
                # -------------------------------------------------

                if response.get("action") == "complete":

                    completed_topics = response.get(
                        "completed_topics",
                        st.session_state.get(
                            "completed_topics",
                            []
                        )
                    )

                    st.session_state.completed_topics = (
                        completed_topics
                    )

                    st.session_state.learning_completed = True

                    st.session_state.agent_stage = "complete"

                    st.success(
                        "Learning path completed successfully."
                    )

                    st.write(
                        "EduPilot identified the student's weak topics, "
                        "adapted the teaching strategy, evaluated learning "
                        "progress, and completed the personalized learning path."
                    )

                    st.write(
                        response.get(
                            "message",
                            "All identified weak topics have been completed."
                        )
                    )

                    st.write("")

                    if st.button(
                        "Back to Dashboard",
                        type="primary"
                    ):
                        go_to(PAGE_DASHBOARD)
                        st.rerun()

                    return

                # -------------------------------------------------
                # Store previous topic
                # -------------------------------------------------

                st.session_state.previous_topic = response.get(
                    "previous_topic",
                    st.session_state.topic
                )

                # -------------------------------------------------
                # Store NEXT topic
                # -------------------------------------------------

                st.session_state.topic = response.get(
                    "topic",
                    st.session_state.topic
                )
                completed_topic = response.get(
                    "previous_topic"
                )

                if (
                    completed_topic
                    and completed_topic not in st.session_state.completed_topics
                ):
                    st.session_state.completed_topics.append(
                        completed_topic
                    )

                # -------------------------------------------------
                # Store next topic mastery
                # -------------------------------------------------

                st.session_state.mastery_score = response.get(
                    "mastery",
                    0
                )

                # -------------------------------------------------
                # Store strategy
                # -------------------------------------------------

                st.session_state.strategy = response.get(
                    "strategy",
                    st.session_state.strategy
                )

                # -------------------------------------------------
                # Store weakness analysis
                # -------------------------------------------------

                st.session_state.weakness_analysis = response.get(
                    "weakness_analysis",
                    ""
                )

                # -------------------------------------------------
                # Store generated lesson
                # -------------------------------------------------

                st.session_state.lesson = response.get(
                    "lesson",
                    ""
                )

                # -------------------------------------------------
                # Clear old quiz
                # -------------------------------------------------

                st.session_state.learning_quiz_questions = []

                st.session_state.learning_quiz_answers = {}

                # -------------------------------------------------
                # Mark next topic as loaded
                # -------------------------------------------------

                st.session_state._next_topic_loaded = True

            except api_client.APIError as exc:

                st.error(exc.message)

                return

        # -----------------------------------------------------
        # Display next topic
        # -----------------------------------------------------

        st.success(
            "Topic mastered. Moving to the next weak topic."
        )

        st.write(
            f"**Completed topic:** "
            f"{st.session_state.get('previous_topic', 'Previous topic')}"
        )

        st.write(
            f"**Next topic:** "
            f"{st.session_state.topic}"
        )

        st.write("---")

        # -----------------------------------------------------
        # Next topic information
        # -----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Current Mastery",
                f"{st.session_state.mastery_score}%"
            )

        with col2:

            st.metric(
                "Teaching Strategy",
                _strategy_label(
                    st.session_state.strategy
                )
            )

        # -----------------------------------------------------
        # Why this topic?
        # -----------------------------------------------------

        with st.expander("Why this topic?"):

            st.write(
                st.session_state.weakness_analysis
                or "No analysis available."
            )

        st.write("---")

        # -----------------------------------------------------
        # New lesson
        # -----------------------------------------------------

        st.markdown("### New Lesson")

        st.markdown(
            st.session_state.lesson
            or "No lesson content was returned."
        )

        st.write("")

        # -----------------------------------------------------
        # Continue learning
        # -----------------------------------------------------

        if st.button(
            "Continue to Next Topic",
            type="primary"
        ):

            st.session_state._next_topic_loaded = False

            st.session_state.agent_stage = "teach"

            go_to(PAGE_LEARNING)

            st.rerun()

        return

    # =========================================================
    # HUMAN INTERVENTION
    # =========================================================

    if action == "human_intervention":

        st.warning(
            "EduPilot recommends a review with a teacher after "
            "multiple adaptation attempts didn't raise mastery enough."
        )

        st.write("")

        if st.button(
            "Back to Dashboard",
            type="primary"
        ):

            go_to(PAGE_DASHBOARD)

            st.rerun()

        return

    # =========================================================
    # TEACH AGAIN
    # =========================================================

    st.info(
        "Your mastery is still below the required level, so "
        "EduPilot changed the teaching strategy."
    )

    st.session_state.agent_stage = "adapt"

    # ---------------------------------------------------------
    # Adaptation already performed
    # ---------------------------------------------------------

    if st.session_state._adapted:

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Previous strategy**")

            st.write(
                _strategy_label(
                    st.session_state.previous_strategy
                )
            )

        with col2:

            st.write("**New strategy**")

            st.write(
                _strategy_label(
                    st.session_state.strategy
                )
            )

        st.write("---")

        st.markdown("### New Lesson")

        st.markdown(
            st.session_state.lesson
            or "No lesson content was returned."
        )

        st.write("")

        if st.button(
            "Continue Learning",
            type="primary"
        ):

            st.session_state._adapted = False

            st.session_state.agent_stage = "teach"

            go_to(PAGE_LEARNING)

            st.rerun()

    # ---------------------------------------------------------
    # Request adaptation from backend
    # ---------------------------------------------------------

    else:

        try:

            with st.spinner(
                "EduPilot is adapting your learning strategy..."
            ):

                response = api_client.adapt_learning(
                    st.session_state.learning_id
                )

        except api_client.APIError as exc:

            st.error(exc.message)

            return

        st.session_state.previous_strategy = response.get(
            "previous_strategy"
        )

        st.session_state.strategy = response.get(
            "new_strategy"
        )

        st.session_state.topic = response.get(
            "topic",
            st.session_state.topic
        )

        st.session_state.weakness_analysis = response.get(
            "weakness_analysis"
        )

        st.session_state.lesson = response.get(
            "lesson"
        )

        st.session_state.mastery_score = response.get(
            "mastery"
        )

        st.session_state.adaptation_attempts = response.get(
            "adaptation_attempts",
            st.session_state.adaptation_attempts
        )

        st.session_state._adapted = True

        st.rerun()