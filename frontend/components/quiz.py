import streamlit as st


def render_questions(questions: list, key_prefix: str) -> dict:
    """
    Renders a vertical list of multiple-choice questions.

    - No option is pre-selected (st.radio index=None).
    - Correctness is never shown here; only options are displayed.

    Returns: {question_id: selected_option_text} for every question the
    student has answered so far (unanswered questions are simply absent).
    """
    answers = {}

    if not questions:
        st.warning("No questions were returned by the backend.")
        return answers

    for position, question in enumerate(questions, start=1):
        question_id = question.get("question_id")
        question_text = question.get("question", "")
        options = question.get("options", [])

        st.markdown(f"**{position}. {question_text}**")

        if not options:
            st.caption("This question has no options available.")
            st.write("")
            continue

        widget_key = f"{key_prefix}_{question_id}"

        selected = st.radio(
            label="Options",
            options=options,
            index=None,
            key=widget_key,
            label_visibility="collapsed",
        )

        if selected is not None:
            answers[question_id] = selected

        st.write("")

    return answers


def all_answered(questions: list, answers: dict) -> bool:
    if not questions:
        return False
    question_ids = {q.get("question_id") for q in questions}
    return question_ids.issubset(set(answers.keys())) and len(answers) == len(questions)