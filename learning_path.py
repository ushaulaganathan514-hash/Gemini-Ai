def generate_learning_path(topic, level="Beginner", weeks=4):

    return {
        "topic": topic,
        "level": level,
        "weeks": weeks,
        "learning_path": [
            {
                "week": 1,
                "title": "Introduction",
                "topics": [
                    f"Introduction to {topic}",
                    "Basic concepts",
                    "Important terminology"
                ]
            },
            {
                "week": 2,
                "title": "Fundamentals",
                "topics": [
                    f"{topic} fundamentals",
                    "Basic examples",
                    "Practice exercises"
                ]
            },
            {
                "week": 3,
                "title": "Practical Learning",
                "topics": [
                    "Practical concepts",
                    "Hands-on exercises",
                    "Mini practice project"
                ]
            },
            {
                "week": 4,
                "title": "Revision and Project",
                "topics": [
                    "Revision",
                    "Problem solving",
                    "Final mini project"
                ]
            }
        ]
    }