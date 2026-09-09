from services.llm_service import get_llm
from rag.retriever import retrieve_knowledge


def generate_lesson(
    topic,
    strategy,
    weakness_analysis
):
    """
    Generate a personalized lesson.

    The system first retrieves relevant material from the
    local knowledge base. It then tries Gemini for a polished
    explanation. If Gemini quota is exhausted, the system
    falls back to the retrieved educational material instead
    of crashing.
    """

    # Retrieve educational material from local RAG
    retrieval_query = f"""
    Topic: {topic}

    Student weakness:
    {weakness_analysis}

    Teaching strategy:
    {strategy}
    """

    retrieved_documents = retrieve_knowledge(
        query=retrieval_query,
        k=4
    )

    knowledge_context = "\n\n".join(
        [
            document["content"]
            for document in retrieved_documents
        ]
    )

    # Determine teaching instruction
    if strategy == "concept_explanation":

        instruction = """
Explain the concept from the basics.
Assume the student has very little knowledge.
Use simple language and a small example.
"""

    elif strategy == "worked_examples":

        instruction = """
Teach the concept using step-by-step worked examples.
Explain why each step is necessary.
"""

    elif strategy == "practice_questions":

        instruction = """
Give a concise explanation followed by several practice examples.
Focus on common mistakes.
"""

    else:

        instruction = """
Provide a deeper explanation with challenging examples.
"""

    # If RAG did not return anything, provide a safe fallback
    if not knowledge_context.strip():

        return f"""
## {topic}

### Personalized Learning

You are currently working on **{topic}**.

Your current learning strategy is:

**{strategy.replace("_", " ").title()}**

Based on your assessment, the identified weakness is:

{weakness_analysis}

The knowledge base did not return enough educational material
to generate a detailed lesson.

Please review the core concepts of {topic} before attempting
the next practice quiz.
"""

    prompt = f"""
You are EduPilot, an adaptive AI tutor.

The student is struggling with:

Topic:
{topic}

Teaching strategy:
{strategy}

Analysis of the student's weakness:
{weakness_analysis}

Below is educational material retrieved
from the student's knowledge base.

---------------- KNOWLEDGE BASE ----------------

{knowledge_context}

-------------- END KNOWLEDGE BASE --------------

{instruction}

IMPORTANT:

- Base the explanation primarily on the provided
  educational material.
- Do not invent facts that contradict the material.
- If the material does not contain enough information,
  clearly say so.
- Keep the explanation easy to understand.
- Use examples when appropriate.
"""

    # Try Gemini
    try:
        llm = get_llm()
        response = llm.invoke(prompt)
        return response.content

    except Exception as exc:

        # Gemini free-tier quota exhausted
        error_text = str(exc)

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):

            print(
                "Gemini quota exhausted. "
                "Using RAG fallback lesson."
            )

            return f"""
## {topic}

### Personalized Lesson

Based on your diagnostic assessment, you need additional
support with **{topic}**.

**Your current weakness:**

{weakness_analysis}

**Recommended strategy:**

{strategy.replace("_", " ").title()}

### Study Material

The following explanation is taken from your educational
knowledge base:

---

{knowledge_context}

---

### What to Focus On

Study the material above carefully and focus especially on
the areas related to your identified weakness.

After reviewing this lesson, take the understanding quiz
to measure your mastery again.
"""

        # Re-raise unexpected errors
        raise