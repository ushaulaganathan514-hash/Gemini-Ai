import json

from google.genai import errors
from gemini_client import get_client
from config import settings


def fallback_quiz(topic, difficulty, count):
    questions = [
        {
            "question": "What is Python?",
            "options": [
                "A programming language",
                "A database",
                "An operating system",
                "A web browser"
            ],
            "correct_answer": "A programming language",
            "explanation": "Python is a popular high-level programming language."
        },
        {
            "question": "Which symbol is used for a comment in Python?",
            "options": [
                "#",
                "//",
                "/* */",
                "<!-- -->"
            ],
            "correct_answer": "#",
            "explanation": "Python uses # for single-line comments."
        },
        {
            "question": "Which function is used to display output in Python?",
            "options": [
                "print()",
                "display()",
                "show()",
                "output()"
            ],
            "correct_answer": "print()",
            "explanation": "The print() function displays output on the screen."
        },
        {
            "question": "Which keyword is used to define a function in Python?",
            "options": [
                "def",
                "function",
                "fun",
                "define"
            ],
            "correct_answer": "def",
            "explanation": "The def keyword is used to define a function."
        },
        {
            "question": "Which data type stores True or False?",
            "options": [
                "Boolean",
                "String",
                "Integer",
                "Float"
            ],
            "correct_answer": "Boolean",
            "explanation": "Boolean values represent True or False."
        }
    ]

    return questions[:count]


def generate_quiz(topic: str, difficulty: str, count: int):

    try:
        client = get_client()

        prompt = f"""
Create exactly {count} multiple-choice questions about {topic}.

Difficulty: {difficulty}

Return ONLY valid JSON.

Format:
{{
    "questions": [
        {{
            "question": "Question",
            "options": [
                "Option 1",
                "Option 2",
                "Option 3",
                "Option 4"
            ],
            "correct_answer": "Option 1",
            "explanation": "Short explanation"
        }}
    ]
}}

Rules:
1. Create exactly {count} questions.
2. Each question must have exactly 4 options.
3. correct_answer must match one option exactly.
4. Return JSON only.
"""

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt
        )

        text = (response.text or "").strip()

        text = text.replace("```json", "").replace("```", "").strip()

        quiz_data = json.loads(text)

        if isinstance(quiz_data, dict):
            questions = quiz_data.get("questions", [])
        elif isinstance(quiz_data, list):
            questions = quiz_data
        else:
            questions = []

        return {
            "topic": topic,
            "difficulty": difficulty,
            "count": len(questions),
            "quiz": {
                "questions": questions
            }
        }

    except Exception as e:

        # Gemini quota/error → use sample quiz
        questions = fallback_quiz(topic, difficulty, count)

        return {
            "topic": topic,
            "difficulty": difficulty,
            "count": len(questions),
            "quiz": {
                "questions": questions
            },
            "error": None
        }