from agent.graph import build_agent


agent = build_agent()


initial_state = {
    "student_id": "ST001",
    "goal": "Score 80% in DBMS",
    "subject": "DBMS",
    "target_score": 80.0,
}


result = agent.invoke(initial_state)



print(": FINAL STATE :")


print(result)