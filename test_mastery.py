from services.mastery_service import (
    calculate_mastery,
    identify_weak_topics
)


topic_stats = {
    "ER Model": {
        "total": 2,
        "correct": 2,
        "incorrect": 0
    },

    "SQL": {
        "total": 3,
        "correct": 1,
        "incorrect": 2
    },

    "Normalization": {
        "total": 3,
        "correct": 0,
        "incorrect": 3
    },

    "Transactions": {
        "total": 2,
        "correct": 2,
        "incorrect": 0
    }
}


mastery = calculate_mastery(topic_stats)

print("Mastery Scores:")
print(mastery)

weak_topics = identify_weak_topics(mastery)

print("\nWeak Topics:")
print(weak_topics)