from services.llm_service import get_llm


llm = get_llm()

response = llm.invoke(
    "who is priyanka chopra and what is her net worth?"
)

print(response.content)