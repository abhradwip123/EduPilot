import streamlit as st

import api_client
from state import go_to, PAGE_ADAPTIVE_RESULT
from components.agent_status import render_agent_workflow
from components.progress import render_progress
from components.quiz import render_questions, all_answered


def render():
    render_agent_workflow(st.session_state.agent_stage)
    st.write("")

    st.subheader("Check Your Understanding")
    st.write("")

    questions = st.session_state.learning_quiz_questions

    if not questions:
        st.error("No quiz questions available. Please return to your lesson.")
        return

    answers = render_questions(
        questions,
        key_prefix="lquiz"
    )

    st.session_state.learning_quiz_answers = answers

    render_progress(
        len(answers),
        len(questions)
    )

    ready = all_answered(
        questions,
        answers
    )

    if not ready:
        st.caption(
            "Please answer all questions before submitting."
        )

    if st.button(
        "Submit Quiz",
        type="primary",
        disabled=not ready
    ):

        try:

            with st.spinner(
                "EduPilot is evaluating your quiz..."
            ):

                response = api_client.submit_learning_quiz(

                    learning_id=st.session_state.learning_id,

                    student_id=st.session_state.student_id,

                    answers=answers,
                )

            # ------------------------------------------------
            # Store quiz result
            # ------------------------------------------------

            previous_mastery = response.get(
                "previous_mastery"
            )

            new_mastery = response.get(
                "new_mastery"
            )

            st.session_state.previous_mastery = (
                previous_mastery
            )

            st.session_state.new_mastery = (
                new_mastery
            )

            st.session_state.adaptation_attempts = (
                response.get(
                    "adaptation_attempts",
                    0
                )
            )

            st.session_state.decision = (
                response.get(
                    "decision",
                    {}
                )
            )

            st.session_state.quiz_results = (
                response.get(
                    "quiz_results"
                )
            )
            # ------------------------------------------------
            # Record learning activity
            # ------------------------------------------------

            history_entry = {
                "topic": st.session_state.topic,
                "previous_mastery": previous_mastery,
                "new_mastery": new_mastery,
                "strategy": st.session_state.strategy,
                "adaptation_attempt": st.session_state.adaptation_attempts,
            }

            st.session_state.learning_history.append(
                history_entry
            )

            # ------------------------------------------------
            # Update mastery for the current topic
            # ------------------------------------------------

            current_topic = st.session_state.topic

            if (
                current_topic
                and new_mastery is not None
            ):

                st.session_state.mastery_scores[
                    current_topic
                ] = new_mastery

            # ------------------------------------------------
            # Update weak topics
            #
            # A topic with mastery >= 70% is no longer weak.
            # ------------------------------------------------

            if (
                current_topic
                and new_mastery is not None
                and new_mastery >= 70
            ):

                weak_topics = (
                    st.session_state.get(
                        "weak_topics",
                        []
                    )
                )

                if current_topic in weak_topics:

                    weak_topics.remove(
                        current_topic
                    )

                st.session_state.weak_topics = (
                    weak_topics
                )

            # ------------------------------------------------
            # Track completed topic
            #
            # If this quiz has brought the topic to mastery,
            # mark it as completed.
            # ------------------------------------------------

            if (
                current_topic
                and new_mastery is not None
                and new_mastery >= 70
            ):

                completed_topics = (
                    st.session_state.get(
                        "completed_topics",
                        []
                    )
                )

                if current_topic not in completed_topics:

                    completed_topics.append(
                        current_topic
                    )

                st.session_state.completed_topics = (
                    completed_topics
                )

            # ------------------------------------------------
            # Prepare adaptive result page
            # ------------------------------------------------

            st.session_state.previous_strategy = (
                st.session_state.strategy
            )

            st.session_state._adapted = False

            st.session_state.agent_stage = (
                "evaluate"
            )

            go_to(
                PAGE_ADAPTIVE_RESULT
            )

            st.rerun()

        except api_client.APIError as exc:

            st.error(
                exc.message
            )