import json
import random
from pathlib import Path


QUESTIONS_FILE = Path("data/sample/questions.json")


def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_quiz(topic: str, num_questions: int = 3):
    """
    Generate a learning quiz from the local question bank.

    This version does not call Gemini, so it works even when
    the Gemini API quota has been exhausted.
    """

    questions = load_questions()

    topic_questions = [
        q for q in questions
        if q.get("topic", "").lower() == topic.lower()
    ]

    if not topic_questions:
        raise ValueError(
            f"No questions found for topic '{topic}'."
        )

    if len(topic_questions) < num_questions:
        num_questions = len(topic_questions)

    selected_questions = random.sample(
        topic_questions,
        num_questions
    )

    return selected_questions