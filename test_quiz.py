from tools.quiz_tool import generate_quiz


quiz = generate_quiz(
    topic="Normalization",
    num_questions=3
)


for i, question in enumerate(quiz, start=1):

    print(f"\nQuestion {i}")
    print(question["question"])

    for option in question["options"]:
        print("-", option)

    print("Correct answer:", question["answer"])