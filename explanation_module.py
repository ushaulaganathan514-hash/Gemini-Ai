from google import genai
from config import settings


def fallback_explanation(concept):

    c = concept.lower().strip()

    if "artificial intelligence" in c or c == "ai":
        return (
            "Artificial Intelligence (AI) is a technology that enables computers "
            "to perform tasks that normally require human intelligence. "
            "Examples include learning, problem solving, speech recognition, "
            "and image recognition."
        )

    if "python" in c:
        return (
            "Python is a high-level programming language known for its simple "
            "syntax and readability. It is widely used in web development, "
            "data science, artificial intelligence, automation, and software development."
        )

    if "java" in c:
        return (
            "Java is a high-level, object-oriented programming language. "
            "It is commonly used for desktop applications, web applications, "
            "Android development, and enterprise software."
        )

    if "html" in c:
        return (
            "HTML stands for HyperText Markup Language. "
            "It is used to create the basic structure of web pages using elements "
            "such as headings, paragraphs, links, images, and forms."
        )

    if "css" in c:
        return (
            "CSS stands for Cascading Style Sheets. "
            "It is used to control the appearance of web pages, including "
            "colors, fonts, spacing, layouts, and responsive design."
        )

    return (
        f"{concept} is an important concept in computer science. "
        "It can be understood by learning its definition, basic concepts, "
        "examples, applications, and practical uses."
    )


def explain_concept(concept):

    try:

        client = genai.Client(
            api_key=settings.gemini_api_key
        )

        prompt = f"""
Explain the following concept to a college student.

Concept:
{concept}

Give the explanation in a simple and clear way.

Include:
1. Definition
2. Main points
3. Simple example
4. Real-world application

Do not use unnecessary technical language.
"""

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt
        )

        answer = response.text or ""

        if answer.strip():
            return answer

        return fallback_explanation(concept)

    except Exception:

        return fallback_explanation(concept)