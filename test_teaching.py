from services.adaptation_service import (
    analyze_weakness,
    choose_strategy
)

from tools.teaching_tool import generate_lesson


topic = "Normalization"
mastery_score = 30


analysis = analyze_weakness(
    topic,
    mastery_score
)

strategy = choose_strategy(
    topic,
    mastery_score
)


lesson = generate_lesson(
    topic,
    strategy,
    analysis
)


print(": WEAKNESS ANALYSIS :")


print(analysis)


print(": TEACHING STRATEGY :")


print(strategy)


print(": PERSONALIZED LESSON :")


print(lesson)