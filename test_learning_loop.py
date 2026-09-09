from tools.quiz_tool import generate_quiz
from tools.evaluation_tool import evaluate_answers
from services.mastery_service import calculate_mastery


topic = "Normalization"


quiz = generate_quiz(
    topic,
    num_questions=3
)


student_answers = {}


# Temporary simulation:
# Student gets some answers correct and some wrong.

for index, question in enumerate(quiz):

    if index == 0:
        student_answers[question["id"]] = question["answer"]

    else:
        student_answers[question["id"]] = "WRONG ANSWER"


results = evaluate_answers(
    quiz,
    student_answers
)


mastery = calculate_mastery(
    results["topic_stats"]
)



print(": LEARNING QUIZ RESULT :")



for topic_name, score in mastery.items():

    print(
        f"{topic_name}: {score}%"
    )