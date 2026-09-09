from fastapi import APIRouter, HTTPException
import uuid
from tools.teacher_insight_tool import generate_teacher_recommendation

from backend.schemas import (
    LearningStartRequest,
    LearningStartResponse,
    LearningQuizResponse,
    LearningQuizSubmitRequest,
    QuestionResponse,
)

from backend.assessment_store import assessments
from backend.learning_store import learning_sessions

from services.adaptation_service import (
    analyze_weakness,
    choose_strategy,
    decide_next_action,
)

from tools.teaching_tool import generate_lesson
from tools.quiz_tool import generate_quiz
from tools.evaluation_tool import evaluate_answers

from services.mastery_service import calculate_mastery


router = APIRouter(prefix="/learning", tags=["Learning"])


# ============================================================
# START LEARNING
# ============================================================

@router.post("/start", response_model=LearningStartResponse)
def start_learning(request: LearningStartRequest):

    assessment = assessments.get(request.assessment_id)

    if not assessment:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found"
        )

    if assessment["student_id"] != request.student_id:
        raise HTTPException(
            status_code=403,
            detail="Student does not own this assessment"
        )

    weak_topics = assessment.get("weak_topics", [])

    mastery_scores = assessment.get(
        "mastery_scores",
        {}
    )

    if not weak_topics:
        raise HTTPException(
            status_code=400,
            detail="No weak topics found. Learning session is not required."
        )

    # --------------------------------------------------------
    # Select weakest topic first
    # --------------------------------------------------------

    current_topic = min(
        weak_topics,
        key=lambda topic: mastery_scores.get(topic, 0)
    )

    mastery_score = mastery_scores.get(
        current_topic,
        0
    )

    # --------------------------------------------------------
    # Analyze weakness
    # --------------------------------------------------------

    weakness_analysis = analyze_weakness(
        current_topic,
        mastery_score
    )

    # --------------------------------------------------------
    # Select teaching strategy
    # --------------------------------------------------------

    strategy = choose_strategy(
        current_topic,
        mastery_score
    )

    # --------------------------------------------------------
    # Generate personalized lesson
    # --------------------------------------------------------

    lesson = generate_lesson(
        topic=current_topic,
        strategy=strategy,
        weakness_analysis=weakness_analysis
    )

    # --------------------------------------------------------
    # Create learning session
    # --------------------------------------------------------

    learning_id = str(uuid.uuid4())

    learning_sessions[learning_id] = {

        "student_id": request.student_id,

        "assessment_id": request.assessment_id,

        # All weak topics from diagnostic assessment
        "weak_topics": weak_topics.copy(),

        # Topics already completed
        "completed_topics": [],

        # Current topic
        "topic": current_topic,

        "mastery_score": mastery_score,

        "initial_mastery_score": mastery_score,

        # Teaching strategy
        "strategy": strategy,

        "previous_strategies": [strategy],

        # Weakness analysis
        "weakness_analysis": weakness_analysis,

        # Current lesson
        "lesson": lesson,

        # Quiz state
        "quiz": None,

        "quiz_results": None,

        # Adaptation state
        "adaptation_attempts": 0,

        "decision": None,
    }

    return LearningStartResponse(

        learning_id=learning_id,

        student_id=request.student_id,

        topic=current_topic,

        mastery_score=mastery_score,

        strategy=strategy,

        weakness_analysis=weakness_analysis,

        lesson=lesson
    )


# ============================================================
# GENERATE LEARNING QUIZ
# ============================================================

@router.post(
    "/quiz",
    response_model=LearningQuizResponse
)
def generate_learning_quiz(
    learning_id: str
):

    session = learning_sessions.get(
        learning_id
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Learning session not found"
        )

    quiz = generate_quiz(
        topic=session["topic"],
        num_questions=3
    )

    session["quiz"] = quiz

    formatted_questions = []

    for question in quiz:

        formatted_questions.append(
            QuestionResponse(

                question_id=question["id"],

                question=question["question"],

                topic=question["topic"],

                subtopic=question["subtopic"],

                options=question["options"]
            )
        )

    return LearningQuizResponse(

        learning_id=learning_id,

        topic=session["topic"],

        questions=formatted_questions
    )


# ============================================================
# SUBMIT LEARNING QUIZ
# ============================================================

@router.post("/quiz/submit")
def submit_learning_quiz(
    request: LearningQuizSubmitRequest
):

    session = learning_sessions.get(
        request.learning_id
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Learning session not found"
        )

    if session["student_id"] != request.student_id:
        raise HTTPException(
            status_code=403,
            detail="Student does not own this learning session"
        )

    quiz = session.get("quiz")

    if not quiz:
        raise HTTPException(
            status_code=400,
            detail="Generate the learning quiz first"
        )

    # --------------------------------------------------------
    # Evaluate answers
    # --------------------------------------------------------

    results = evaluate_answers(
        quiz,
        request.answers
    )

    # --------------------------------------------------------
    # Calculate mastery
    # --------------------------------------------------------

    mastery_scores = calculate_mastery(
        results["topic_stats"]
    )

    new_mastery = mastery_scores.get(
        session["topic"],
        0
    )

    # --------------------------------------------------------
    # Increment adaptation attempt
    # --------------------------------------------------------

    attempts = (
        session.get(
            "adaptation_attempts",
            0
        ) + 1
    )

    previous_strategy = session.get(
        "strategy"
    )

    # --------------------------------------------------------
    # Agent decision
    # --------------------------------------------------------

    decision = decide_next_action(

        mastery_score=new_mastery,

        previous_strategy=previous_strategy,

        attempts=attempts
    )

    # --------------------------------------------------------
    # Store results
    # --------------------------------------------------------

    previous_mastery = session.get(
        "mastery_score",
        session.get(
            "initial_mastery_score",
            0
        )
    )

    session["quiz_results"] = results

    session["mastery_score"] = new_mastery

    session["adaptation_attempts"] = attempts

    session["decision"] = decision

    return {

    "learning_id": request.learning_id,

    "topic": session["topic"],

    "previous_mastery": previous_mastery,

    "new_mastery": new_mastery,

    "adaptation_attempts": attempts,

    "decision": decision,

    "quiz_results": results
    }


# ============================================================
# ADAPT LEARNING
# ============================================================

@router.post("/adapt")
def adapt_learning(
    learning_id: str
):

    session = learning_sessions.get(
        learning_id
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Learning session not found"
        )

    decision = session.get(
        "decision"
    )

    if not decision:
        raise HTTPException(
            status_code=400,
            detail="Submit the learning quiz first"
        )

    action = decision.get(
        "action",
        "complete"
    )

    # ========================================================
    # NEXT TOPIC
    # ========================================================

    if action == "next_topic":

        current_topic = session["topic"]

        # ----------------------------------------------------
        # Mark current topic as completed
        # ----------------------------------------------------

        completed_topics = session.get(
            "completed_topics",
            []
        )

        if current_topic not in completed_topics:

            completed_topics.append(
                current_topic
            )

        session["completed_topics"] = (
            completed_topics
        )

        # ----------------------------------------------------
        # Find remaining weak topics
        # ----------------------------------------------------

        weak_topics = session.get(
            "weak_topics",
            []
        )

        remaining_topics = [
            topic
            for topic in weak_topics
            if topic not in completed_topics
        ]

        # ----------------------------------------------------
        # ALL TOPICS COMPLETED
        # ----------------------------------------------------

        if not remaining_topics:

            return {

                "learning_id": learning_id,

                "action": "complete",
                "completed_topics": completed_topics,

                "message": (
                    "All identified weak topics "
                    "have been completed."
                ),

                "mastery": session.get(
                    "mastery_score",
                    0
                )
            }

        # ----------------------------------------------------
        # Get original assessment mastery scores
        # ----------------------------------------------------

        assessment = assessments.get(
            session["assessment_id"]
        )

        if not assessment:

            raise HTTPException(
                status_code=404,
                detail="Assessment not found"
            )

        mastery_scores = assessment.get(
            "mastery_scores",
            {}
        )

        # ----------------------------------------------------
        # Select weakest remaining topic
        # ----------------------------------------------------

        next_topic = min(
            remaining_topics,
            key=lambda topic: mastery_scores.get(
                topic,
                0
            )
        )

        next_mastery = mastery_scores.get(
            next_topic,
            0
        )

        # ----------------------------------------------------
        # Analyze next topic
        # ----------------------------------------------------

        weakness_analysis = analyze_weakness(
            next_topic,
            next_mastery
        )

        # ----------------------------------------------------
        # Choose strategy for next topic
        # ----------------------------------------------------

        strategy = choose_strategy(
            next_topic,
            next_mastery
        )

        # ----------------------------------------------------
        # Generate next lesson
        # ----------------------------------------------------

        lesson = generate_lesson(

            topic=next_topic,

            strategy=strategy,

            weakness_analysis=weakness_analysis
        )

        # ----------------------------------------------------
        # Update session
        # ----------------------------------------------------

        session["topic"] = next_topic

        session["mastery_score"] = next_mastery

        session["initial_mastery_score"] = (
            next_mastery
        )

        session["strategy"] = strategy

        session["previous_strategies"] = [
            strategy
        ]

        session["weakness_analysis"] = (
            weakness_analysis
        )

        session["lesson"] = lesson

        # Reset quiz/adaptation state
        session["quiz"] = None

        session["quiz_results"] = None

        session["decision"] = None

        # ----------------------------------------------------
        # Return next topic
        # ----------------------------------------------------

        return {

            "learning_id": learning_id,

            "action": "next_topic",

            "previous_topic": current_topic,

            "topic": next_topic,

            "mastery": next_mastery,

            "strategy": strategy,

            "weakness_analysis": weakness_analysis,

            "lesson": lesson,

            "message": (
                f"Topic '{current_topic}' mastered. "
                f"Moving to '{next_topic}'."
            )
        }

    # ========================================================
    # TEACH AGAIN
    # ========================================================

    if action == "teach_again":

        topic = session["topic"]

        old_strategy = session.get(
            "strategy"
        )

        # ----------------------------------------------------
        # Choose a new strategy
        # ----------------------------------------------------

        new_strategy = choose_strategy(
            topic,
            session["mastery_score"]
        )

        previous_strategies = session.get(
            "previous_strategies",
            []
        )

        # ----------------------------------------------------
        # Prevent repeating same strategy
        # ----------------------------------------------------

        if new_strategy in previous_strategies:

            strategies = [

                "concept_explanation",

                "worked_examples",

                "practice_questions",

                "advanced_practice",
            ]

            for strategy_option in strategies:

                if strategy_option not in previous_strategies:

                    new_strategy = strategy_option

                    break

        # ----------------------------------------------------
        # Analyze weakness again
        # ----------------------------------------------------

        weakness_analysis = analyze_weakness(

            topic,

            session["mastery_score"]
        )

        # ----------------------------------------------------
        # Generate new lesson
        # ----------------------------------------------------

        lesson = generate_lesson(

            topic=topic,

            strategy=new_strategy,

            weakness_analysis=weakness_analysis
        )

        # ----------------------------------------------------
        # Update strategy history
        # ----------------------------------------------------

        previous_strategies.append(
            new_strategy
        )

        session["strategy"] = (
            new_strategy
        )

        session["previous_strategies"] = (
            previous_strategies
        )

        session["lesson"] = lesson

        session["weakness_analysis"] = (
            weakness_analysis
        )

        return {

            "learning_id": learning_id,

            "action": "teach_again",

            "topic": topic,

            "previous_strategy": old_strategy,

            "new_strategy": new_strategy,

            "mastery": session["mastery_score"],

            "weakness_analysis": weakness_analysis,

            "lesson": lesson,

            "adaptation_attempts": (
                session["adaptation_attempts"]
            )
        }

    # ========================================================
    # COMPLETE / HUMAN INTERVENTION
    # ========================================================

    return {

        "learning_id": learning_id,

        "action": "complete",

        "message": "Learning session completed."
    }
@router.post("/teacher-insights")
def teacher_insights(request: dict):

    mastery_scores = request.get(
        "mastery_scores",
        {}
    )

    weak_topics = request.get(
        "weak_topics",
        []
    )

    learning_history = request.get(
        "learning_history",
        []
    )

    if not mastery_scores:
        return {
            "recommendation": (
                "There is not enough student performance "
                "data to generate a recommendation."
            )
        }

    recommendation = generate_teacher_recommendation(
        mastery_scores=mastery_scores,
        weak_topics=weak_topics,
        learning_history=learning_history,
    )

    return {
        "recommendation": recommendation
    }