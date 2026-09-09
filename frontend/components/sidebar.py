import streamlit as st

from state import (
    go_to,
    reset_everything,
    PAGE_DASHBOARD
)


def render_sidebar():

    with st.sidebar:

        st.subheader("Student Profile")

        locked = (
            st.session_state.assessment_id is not None
        )

        student_id = st.text_input(
            "Student ID",
            value=st.session_state.student_id,
            disabled=locked,
            placeholder="e.g. ST001",
        )

        subject = st.text_input(
            "Subject",
            value=st.session_state.subject,
            disabled=locked,
            placeholder="e.g. DBMS",
        )

        st.session_state.student_id = student_id.strip()
        st.session_state.subject = subject.strip()

        st.session_state.target_score = st.number_input(
            "Target Score (%)",
            min_value=0,
            max_value=100,
            step=5,
            value=st.session_state.target_score,
        )

        st.session_state.exam_date = st.date_input(
            "Exam Date (optional)",
            value=st.session_state.exam_date,
        )

        st.divider()

        st.subheader("Learning Progress")

        if st.session_state.mastery_scores:

            for topic, score in st.session_state.mastery_scores.items():

                st.caption(topic)

                st.progress(
                    min(max(int(score), 0), 100) / 100
                )

        else:

            st.caption(
                "No assessment completed yet."
            )

        st.write(
            f"**Adaptation attempts:** "
            f"{st.session_state.adaptation_attempts}"
        )

        st.divider()

        if st.button(
            "Back to Dashboard",
            use_container_width=True
        ):
            go_to(PAGE_DASHBOARD)
            st.rerun()

        if st.button(
            "Reset Session",
            use_container_width=True
        ):
            reset_everything()
            st.rerun()