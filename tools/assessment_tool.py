import json
import random
from pathlib import Path


QUESTIONS_FILE = Path("data/sample/questions.json")


def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_diagnostic_test(subject: str, num_questions: int = 10):
    questions = load_questions()

    subject_questions = [
        q for q in questions
        if q["subject"].lower() == subject.lower()
    ]

    if len(subject_questions) < num_questions:
        num_questions = len(subject_questions)

    selected_questions = random.sample(
        subject_questions,
        num_questions
    )

    return selected_questions