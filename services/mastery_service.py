def calculate_mastery(topic_stats):

    mastery_scores = {}

    for topic, stats in topic_stats.items():

        total = stats["total"]
        correct = stats["correct"]

        if total == 0:
            mastery = 0

        else:
            mastery = (correct / total) * 100

        mastery_scores[topic] = round(mastery, 2)

    return mastery_scores


def identify_weak_topics(mastery_scores):

    weak_topics = []

    for topic, score in mastery_scores.items():

        if score < 70:
            weak_topics.append(topic)

    return weak_topics