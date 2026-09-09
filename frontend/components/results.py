import streamlit as st


def render_mastery_table(mastery_scores):
    st.markdown("**Mastery by Topic**")

    if not mastery_scores:
        st.info("No mastery scores available yet.")
        return

    for topic, score in mastery_scores.items():
        st.write(f"{topic}")

        col1, col2 = st.columns([8, 1])

        with col1:
            st.progress(min(max(float(score), 0), 100) / 100)

        with col2:
            st.write(f"{float(score):.0f}%")


def render_weak_topics(weak_topics):
    st.markdown("**Weak Topics**")

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