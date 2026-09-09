# EduPilot

**EduPilot** is an Agentic AI-powered adaptive learning system designed to personalize education based on individual student performance.

Instead of providing the same learning path to every student, EduPilot first evaluates the student's knowledge, identifies weak topics, generates a personalized learning plan, teaches the student using an adaptive strategy, evaluates mastery through quizzes, and dynamically decides what the student should learn next.

The system also provides a teacher-focused dashboard with student mastery, weak topics, adaptive learning history, and an AI-generated teacher recommendation.

---

## Problem Statement

Traditional learning systems often provide the same content and difficulty level to every student.

A student may understand some topics well while struggling with others, but many systems do not continuously adapt the learning process based on topic-level performance.

This creates two major problems:

- Students may spend unnecessary time on topics they already understand.
- Teachers may not have a clear picture of which concepts require additional support.

---

## Proposed Solution

EduPilot uses an **Agentic AI adaptive learning workflow** to continuously evaluate and improve the student's learning path.

The system:

1. Conducts a diagnostic assessment.
2. Calculates topic-level mastery.
3. Identifies weak topics.
4. Creates a personalized learning plan.
5. Selects an appropriate teaching strategy.
6. Generates a personalized lesson.
7. Generates a learning quiz.
8. Evaluates the student's performance.
9. Recalculates mastery.
10. Dynamically decides whether to:
   - teach the topic again using a different strategy,
   - move to the next weak topic,
   - or recommend teacher intervention.
11. Tracks the student's learning history.
12. Provides teacher insights and an AI-generated recommendation.

---

## Key Features

### 1. Diagnostic Assessment

EduPilot starts with a diagnostic test to understand the student's current knowledge.

### 2. Topic-Level Weakness Detection

The system calculates mastery for individual topics instead of relying only on one overall score.

### 3. Personalized Learning Plan

Weak topics are prioritized for targeted learning.

### 4. Adaptive Teaching Strategy

The system can change the teaching strategy based on student performance.

Example strategies include:

- Conceptual Explanation
- Worked Examples
- Practice Questions
- Advanced Practice

### 5. AI-Generated Lessons

Gemini is used to generate personalized teaching content based on the student's identified weakness.

### 6. Learning Quiz

After each lesson, EduPilot generates a quiz to evaluate understanding.

### 7. Mastery Evaluation

The system recalculates topic mastery after each learning quiz.

### 8. Adaptive Decision Making

The agent dynamically chooses the next action based on the student's performance.

Possible actions include:

- Teach Again
- Move to Next Topic
- Recommend Teacher Review

### 9. Learning History

EduPilot maintains a history of learning cycles, including:

- Topic
- Previous mastery
- New mastery
- Teaching strategy
- Adaptation event

### 10. Teacher Insights

Teachers can view:

- Overall mastery
- Topic performance
- Topics requiring attention
- Adaptive learning history
- Session summary
- AI-generated teacher recommendation

### 11. RAG-Based Knowledge Retrieval

Educational knowledge is stored in a ChromaDB vector store and retrieved using local HuggingFace embeddings to support the learning process.

---

## System Workflow

```text
Student
   |
   v
Diagnostic Assessment
   |
   v
Evaluate Student Performance
   |
   v
Identify Weak Topics
   |
   v
Create Learning Plan
   |
   v
Analyze Weakness
   |
   v
Select Teaching Strategy
   |
   v
Generate Personalized Lesson
   |
   v
Generate Learning Quiz
   |
   v
Evaluate Quiz
   |
   v
Calculate New Mastery
   |
   v
Adaptive Decision
   |
   +-----------------------+
   |           |           |
   v           v           v
Teach Again  Next Topic  Teacher Review
   |           |           |
   +-----------+-----------+
               |
               v
        Learning Completion
               |
               v
        Teacher Insights
               |
               v
      AI Teacher Recommendation

## Runnable Version

EduPilot is provided as a runnable application through this GitHub repository.

### Steps to Run

1. Clone the repository:

```bash
git clone https://github.com/abhradwip123/EduPilot
cd EduPilot

## Running the Application

EduPilot has two components:

- **FastAPI Backend:** `http://127.0.0.1:8000`
- **Streamlit Frontend:** `http://localhost:8501`

### 1. Start the Backend

From the project root:

```powershell
uvicorn backend.main:app --reload