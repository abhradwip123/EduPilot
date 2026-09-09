from typing import TypedDict, List, Dict, Any


class EduPilotState(TypedDict, total=False):

    student_id: str

    goal: str
    subject: str
    exam_date: str
    target_score: float

    assessment_questions: List[Dict[str, Any]]
    student_answers: Dict[str, str]
    assessment_results: Dict[str, Any]

    topics: List[str]
    weak_topics: List[str]
    mastery_scores: Dict[str, float]

    current_topic: str

    weakness_analysis: str

    current_strategy: str
    previous_strategies: List[str]

    learning_plan: List[Dict[str, Any]]

    learning_quiz: List[Dict[str, Any]]
    learning_quiz_results: Dict[str, Any]

    learning_mastery: float

    adaptation_attempts: int

    agent_decision: Dict[str, Any]

    next_action: str

    final_outcome: str