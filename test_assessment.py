from tools.assessment_tool import generate_diagnostic_test


questions = generate_diagnostic_test("DBMS", 5)

for question in questions:
    print("\nQuestion:", question["question"])
    print("Topic:", question["topic"])
    print("Subtopic:", question["subtopic"])
    print("Options:")

    for option in question["options"]:
        print("-", option)