from services.llm_service import get_llm


def analyze_weakness(topic: str, mastery_score: float) -> str:
    """
    Analyze the student's weakness using their mastery score.
    This version does not require an LLM.
    """

    if mastery_score < 30:
        level = "significant difficulty"
        recommendation = (
            "Start with fundamental concepts and simple examples."
        )
    elif mastery_score < 50:
        level = "weak understanding"
        recommendation = (
            "Review the core concepts and practice worked examples."
        )
    elif mastery_score < 70:
        level = "partial understanding"
        recommendation = (
            "Strengthen the concepts with targeted practice questions."
        )
    else:
        level = "moderate understanding"
        recommendation = (
            "Use advanced practice to close the remaining knowledge gaps."
        )

    return (
        f"The student currently shows {level} in {topic}, "
        f"with a mastery score of {mastery_score:.0f}%. "
        f"{recommendation}"
    )


def choose_strategy(topic: str, mastery_score: float) -> str:
    """
    Select a teaching strategy based on mastery.
    """

    if mastery_score < 30:
        return "concept_explanation"

    if mastery_score < 50:
        return "worked_examples"

    if mastery_score < 70:
        return "practice_questions"

    return "advanced_practice"


def decide_next_action(
    mastery_score: float,
    previous_strategy: str,
    attempts: int
) -> dict:
    """
    Decide what the adaptive agent should do after a quiz.
    """

    # Student has mastered the topic.
    if mastery_score >= 70:
        return {
            "action": "next_topic",
            "reason": (
                f"Mastery reached {mastery_score:.0f}%, "
                "which is sufficient to move to the next topic."
            )
        }

    # Too many unsuccessful attempts.
    if attempts >= 3:
        return {
            "action": "human_intervention",
            "reason": (
                "Mastery is still below the required threshold after "
                "multiple adaptive attempts. Teacher review is recommended."
            )
        }

    # Student needs another teaching strategy.
    return {
        "action": "teach_again",
        "reason": (
            f"Mastery is currently {mastery_score:.0f}%, "
            "so the agent will change the teaching strategy."
        )
    }