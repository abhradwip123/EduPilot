from services.adaptation_service import (
    analyze_weakness,
    choose_strategy
)


topic = "Normalization"
mastery_score = 30


print("Analyzing student weakness...\n")

analysis = analyze_weakness(
    topic,
    mastery_score
)

print("AI Analysis:")
print(analysis)


strategy = choose_strategy(
    topic,
    mastery_score
)

print("\nSelected Strategy:")
print(strategy)