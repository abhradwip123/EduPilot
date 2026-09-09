from services.adaptation_service import (
    analyze_weakness,
    choose_strategy,
    decide_next_action
)

from tools.teaching_tool import generate_lesson

from tools.quiz_tool import generate_quiz


from tools.assessment_tool import generate_diagnostic_test
from tools.evaluation_tool import evaluate_answers
from services.mastery_service import (
    calculate_mastery,
    identify_weak_topics
)


def understand_goal(state):

    print("\n[Agent] Understanding student goal...")

    print(f"Goal: {state['goal']}")
    print(f"Subject: {state['subject']}")
    print(f"Target Score: {state['target_score']}%")

    return {
        "next_action": "assess_student"
    }


def assess_student(state):

    print("\n[Agent] Generating diagnostic assessment...")

    questions = generate_diagnostic_test(
        subject=state["subject"],
        num_questions=10
    )

    print(f"[Agent] Generated {len(questions)} questions.")

    return {
        "assessment_questions": questions,
        "next_action": "evaluate_assessment"
    }


def evaluate_assessment(state):

    print("\n[Agent] Evaluating student assessment...")

    questions = state["assessment_questions"]

    # Temporary answers for testing.
    # Later these will come from Streamlit.
    student_answers = {}

    for question in questions:

        if question["topic"] == "Normalization":
            student_answers[question["id"]] = "WRONG ANSWER"

        elif question["topic"] == "SQL":
            student_answers[question["id"]] = "WRONG ANSWER"

        else:
            student_answers[question["id"]] = question["answer"]

    results = evaluate_answers(
        questions,
        student_answers
    )

    mastery_scores = calculate_mastery(
        results["topic_stats"]
    )

    weak_topics = identify_weak_topics(
        mastery_scores
    )

    print("\n[Agent] Mastery Scores:")

    for topic, score in mastery_scores.items():
        print(f"  {topic}: {score}%")

    print("\n[Agent] Weak Topics:")

    if weak_topics:
        for topic in weak_topics:
            print(f"  - {topic}")
    else:
        print("  No weak topics detected.")

    return {
        "student_answers": student_answers,
        "assessment_results": results,
        "mastery_scores": mastery_scores,
        "weak_topics": weak_topics,
        "next_action": "create_learning_plan"
    }


def create_learning_plan(state):

    print("\n[Agent] Creating learning plan...")

    weak_topics = state.get("weak_topics", [])

    if weak_topics:

        learning_plan = [
            {
                "topic": topic,
                "priority": "HIGH",
                "action": "remedial_learning"
            }
            for topic in weak_topics
        ]

    else:

        learning_plan = [
            {
                "topic": "Continue syllabus",
                "priority": "NORMAL",
                "action": "next_topic"
            }
        ]

    print("\n[Agent] Learning Plan:")

    for item in learning_plan:
        print(
            f"  {item['topic']} "
            f"→ {item['action']}"
        )

    return {
        "learning_plan": learning_plan,
        "next_action": "complete"
    }


def complete(state):

    print("\n[Agent] Assessment workflow completed.")

    weak_topics = state.get("weak_topics", [])

    if weak_topics:

        outcome = (
            f"Identified weak topics: "
            f"{', '.join(weak_topics)}"
        )

    else:

        outcome = "No weak topics detected."

    print(f"[Agent] {outcome}")

    return {
        "final_outcome": outcome
    }
def analyze_student_weakness(state):

    print("\n[Agent] Analyzing student weakness...")

    weak_topics = state.get("weak_topics", [])

    if not weak_topics:

        return {
            "next_action": "complete"
        }

    topic = weak_topics[0]

    mastery_score = state["mastery_scores"].get(
        topic,
        0
    )

    analysis = analyze_weakness(
        topic,
        mastery_score
    )

    strategy = choose_strategy(
        topic,
        mastery_score
    )

    print(f"[Agent] Current topic: {topic}")
    print(f"[Agent] Mastery: {mastery_score}%")
    print(f"[Agent] Strategy: {strategy}")

    return {
        "current_topic": topic,
        "weakness_analysis": analysis,
        "current_strategy": strategy,
        "previous_strategies": [strategy],
        "adaptation_attempts": 0,
        "next_action": "teach_student"
    }


def teach_student(state):

    print("\n[Agent] Teaching student...")

    lesson = generate_lesson(
        topic=state["current_topic"],
        strategy=state["current_strategy"],
        weakness_analysis=state["weakness_analysis"]
    )

    print("\n[Agent] Lesson generated.")

    print("\n------------------------------")
    print(lesson)
    print("------------------------------")

    return {
        "next_action": "generate_learning_quiz"
    }


def generate_learning_quiz(state):

    print("\n[Agent] Generating learning quiz...")

    quiz = generate_quiz(
        topic=state["current_topic"],
        num_questions=3
    )

    return {
        "learning_quiz": quiz,
        "next_action": "evaluate_learning"
    }


def evaluate_learning(state):

    print("\n[Agent] Evaluating learning quiz...")

    quiz = state["learning_quiz"]

    # Temporary simulation.
    # Later Streamlit will collect real answers.

    student_answers = {}

    for index, question in enumerate(quiz):

        if index == 0:

            student_answers[
                question["id"]
            ] = question["answer"]

        else:

            student_answers[
                question["id"]
            ] = "WRONG ANSWER"

    results = evaluate_answers(
        quiz,
        student_answers
    )

    mastery = calculate_mastery(
        results["topic_stats"]
    )

    score = mastery.get(
        state["current_topic"],
        0
    )

    attempts = state.get(
        "adaptation_attempts",
        0
    ) + 1

    previous_strategy = state.get(
        "current_strategy"
    )

    decision = decide_next_action(
        mastery_score=score,
        previous_strategy=previous_strategy,
        attempts=attempts
    )

    print(f"[Agent] New mastery: {score}%")
    print(f"[Agent] Decision: {decision['action']}")
    print(f"[Agent] Reason: {decision['reason']}")

    return {
        "learning_quiz_results": results,
        "learning_mastery": score,
        "agent_decision": decision,
        "adaptation_attempts": attempts,
        "next_action": decision["action"]
    }