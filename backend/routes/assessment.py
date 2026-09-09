import uuid

from fastapi import APIRouter, HTTPException

from backend.schemas import (
    AssessmentStartRequest,
    AssessmentStartResponse,
    QuestionResponse,
    AssessmentSubmitRequest
)

from backend.assessment_store import assessments

from tools.assessment_tool import generate_diagnostic_test

from tools.evaluation_tool import evaluate_answers

from services.mastery_service import (
    calculate_mastery,
    identify_weak_topics
)


router = APIRouter(
    prefix="/assessment",
    tags=["Assessment"]
)


@router.get("/test")
def assessment_test():

    return {
        "message": "Assessment API is working"
    }


@router.post(
    "/start",
    response_model=AssessmentStartResponse
)
def start_assessment(
    request: AssessmentStartRequest
):

    questions = generate_diagnostic_test(
        subject=request.subject,
        num_questions=request.num_questions
    )

    if not questions:

        raise HTTPException(
            status_code=404,
            detail=f"No questions found for subject: {request.subject}"
        )

    assessment_id = str(uuid.uuid4())

    assessments[assessment_id] = {
        "student_id": request.student_id,
        "subject": request.subject,
        "questions": questions,
        "answers": {}
    }

    formatted_questions = []

    for question in questions:

        formatted_questions.append(
            QuestionResponse(
                question_id=question["id"],
                question=question["question"],
                topic=question["topic"],
                subtopic=question["subtopic"],
                options=question["options"]
            )
        )

    return AssessmentStartResponse(
        assessment_id=assessment_id,
        student_id=request.student_id,
        subject=request.subject,
        total_questions=len(questions),
        questions=formatted_questions
    )
@router.post("/submit")
def submit_assessment(
    request: AssessmentSubmitRequest
):

    assessment = assessments.get(
        request.assessment_id
    )

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

    questions = assessment["questions"]

    results = evaluate_answers(
        questions,
        request.answers
    )

    mastery_scores = calculate_mastery(
        results["topic_stats"]
    )

    weak_topics = identify_weak_topics(
        mastery_scores
    )

    assessment["answers"] = request.answers
    assessment["results"] = results
    assessment["mastery_scores"] = mastery_scores
    assessment["weak_topics"] = weak_topics

    return {
        "assessment_id": request.assessment_id,
        "student_id": request.student_id,
        "subject": assessment["subject"],
        "evaluation": results,
        "mastery_scores": mastery_scores,
        "weak_topics": weak_topics
    }