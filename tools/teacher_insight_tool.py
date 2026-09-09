import json

from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import GEMINI_API_KEY


def generate_teacher_recommendation(
    mastery_scores: dict,
    weak_topics: list,
    learning_history: list,
) -> str:

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.3,
    )

    prompt = f"""
You are EduPilot, an adaptive learning system.

Analyze the student's learning data and provide a concise
recommendation for a teacher.

Student mastery:
{json.dumps(mastery_scores, indent=2)}

Weak topics:
{json.dumps(weak_topics, indent=2)}

Learning history:
{json.dumps(learning_history, indent=2)}

Give the teacher:

1. Overall student performance
2. Most important weak areas
3. What the teacher should focus on
4. Whether teacher intervention is recommended

Do not invent information that is not present in the data.

Keep the response practical and concise.
Use simple educational language.
"""

    response = llm.invoke(prompt)

    return response.content