from pydantic import BaseModel
from typing import List, Dict


class AssessmentStartRequest(BaseModel):
    student_id: str
    subject: str
    num_questions: int = 10


class QuestionResponse(BaseModel):
    question_id: str
    question: str
    topic: str
    subtopic: str
    options: List[str]


class AssessmentStartResponse(BaseModel):
    assessment_id: str
    student_id: str
    subject: str
    total_questions: int
    questions: List[QuestionResponse]


class AssessmentSubmitRequest(BaseModel):
    assessment_id: str
    student_id: str
    answers: Dict[str, str]

class LearningStartRequest(BaseModel):
    assessment_id: str
    student_id: str

class LearningStartResponse(BaseModel):
    learning_id: str
    student_id: str
    topic: str
    mastery_score: float
    strategy: str
    weakness_analysis: str
    lesson: str

class LearningQuizResponse(BaseModel):
    learning_id: str
    topic: str
    questions: List[QuestionResponse]


class LearningQuizSubmitRequest(BaseModel):
    learning_id: str
    student_id: str
    answers: Dict[str, str]