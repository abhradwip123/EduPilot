from rag.retriever import retrieve_knowledge


query = """
Explain normalization in DBMS,
especially 1NF, 2NF, 3NF,
partial dependency and transitive dependency.
"""


results = retrieve_knowledge(
    query,
    k=4
)



print("RETRIEVED KNOWLEDGE")



for index, result in enumerate(
    results,
    start=1
):

    print(
        f"\n--- Result {index} ---"
    )

    print(
        "Source:",
        result["source"]
    )

    print(
        result["content"]
    )