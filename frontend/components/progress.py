import streamlit as st


def render_progress(current_answered: int, total: int):
    """Shows 'Question X of Y · Z% completed' plus a progress bar."""
    percent = int((current_answered / total) * 100) if total else 0
    st.caption(f"Question {current_answered} of {total}  ·  {percent}% completed")
    st.progress(percent / 100 if total else 0.0)