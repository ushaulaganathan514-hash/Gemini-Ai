from google import genai
from google.genai import errors
from config import settings


def fallback_answer(question: str):

    q = question.lower().strip()

    if "what is python" in q:
        return "Python is a high-level, easy-to-learn programming language used for web development, data science, artificial intelligence, automation, and many other applications."

    if "what is java" in q:
        return "Java is a high-level, object-oriented programming language used to build desktop, web, mobile, and enterprise applications."

    if "what is ai" in q or "artificial intelligence" in q:
        return "Artificial Intelligence (AI) is a technology that enables computers to perform tasks that normally require human intelligence, such as learning, reasoning, and understanding language."

    if "what is html" in q:
        return "HTML stands for HyperText Markup Language. It is used to create the structure of web pages."

    if "what is css" in q:
        return "CSS stands for Cascading Style Sheets. It is used to style and design web pages."

    return "This is a sample educational answer. Gemini AI is currently unavailable because the API quota has been exhausted. Please try again after the quota resets."


def answer_question(question: str):

    try:

        client = genai.Client(api_key=settings.gemini_api_key)

        prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the student's question clearly and accurately.

Student question:
{question}

Give a simple explanation suitable for a college student.
"""

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt
        )

        return {
            "question": question,
            "answer": response.text or "",
            "error": None
        }

    except Exception:

        return {
            "question": question,
            "answer": fallback_answer(question),
            "error": None
        }