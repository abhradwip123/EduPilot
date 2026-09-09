from collections import defaultdict


def evaluate_answers(questions, student_answers):

    topic_stats = defaultdict(
        lambda: {
            "total": 0,
            "correct": 0,
            "incorrect": 0
        }
    )

    question_results = []

    for question in questions:

        question_id = question["id"]

        student_answer = student_answers.get(question_id)

        correct_answer = question["answer"]

        is_correct = (
            student_answer == correct_answer
        )

        topic = question["topic"]

        topic_stats[topic]["total"] += 1

        if is_correct:
            topic_stats[topic]["correct"] += 1
        else:
            topic_stats[topic]["incorrect"] += 1

        question_results.append({
            "question_id": question_id,
            "topic": topic,
            "subtopic": question["subtopic"],
            "student_answer": student_answer,
            "correct_answer": correct_answer,
            "correct": is_correct
        })

    return {
        "topic_stats": dict(topic_stats),
        "question_results": question_results
    }