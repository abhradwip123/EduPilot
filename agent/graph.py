from langgraph.graph import StateGraph, START, END

from agent.state import EduPilotState

from agent.nodes import (
    understand_goal,
    assess_student,
    evaluate_assessment,
    create_learning_plan,
    complete,
    analyze_student_weakness,
    teach_student,
    generate_learning_quiz,
    evaluate_learning
)


def route_after_assessment(state):

    weak_topics = state.get(
        "weak_topics",
        []
    )

    if weak_topics:

        return "analyze_weakness"

    return "complete"


def route_after_learning(state):

    decision = state.get(
        "agent_decision",
        {}
    )

    action = decision.get(
        "action",
        "complete"
    )

    if action == "teach_again":

        return "teach_again"

    if action == "next_topic":

        return "complete"

    if action == "human_intervention":

        return "complete"

    return "complete"


def build_agent():

    graph = StateGraph(EduPilotState)

    
    # Nodes
    

    graph.add_node(
        "understand_goal",
        understand_goal
    )

    graph.add_node(
        "assess_student",
        assess_student
    )

    graph.add_node(
        "evaluate_assessment",
        evaluate_assessment
    )

    graph.add_node(
        "create_learning_plan",
        create_learning_plan
    )

    graph.add_node(
        "analyze_weakness",
        analyze_student_weakness
    )

    graph.add_node(
        "teach_student",
        teach_student
    )

    graph.add_node(
        "generate_learning_quiz",
        generate_learning_quiz
    )

    graph.add_node(
        "evaluate_learning",
        evaluate_learning
    )

    graph.add_node(
        "complete",
        complete
    )

    
    # Initial workflow
    

    graph.add_edge(
        START,
        "understand_goal"
    )

    graph.add_edge(
        "understand_goal",
        "assess_student"
    )

    graph.add_edge(
        "assess_student",
        "evaluate_assessment"
    )

    
    # Agent decision
    
    graph.add_conditional_edges(
        "evaluate_assessment",
        route_after_assessment,
        {
            "analyze_weakness": "analyze_weakness",
            "complete": "complete"
        }
    )

    
    # Adaptive learning
    

    graph.add_edge(
        "analyze_weakness",
        "teach_student"
    )

    graph.add_edge(
        "teach_student",
        "generate_learning_quiz"
    )

    graph.add_edge(
        "generate_learning_quiz",
        "evaluate_learning"
    )

    
    # Adaptation decision
   
    graph.add_conditional_edges(
        "evaluate_learning",
        route_after_learning,
        {
            "teach_again": "teach_student",
            "complete": "complete"
        }
    )

    
    # End
    

    graph.add_edge(
        "complete",
        END
    )

    return graph.compile()