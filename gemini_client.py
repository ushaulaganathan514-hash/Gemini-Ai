from functools import lru_cache

from google import genai

from config import settings


@lru_cache(maxsize=1)
def get_client():
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Please add it to the .env file."
        )

    return genai.Client(api_key=settings.gemini_api_key)


def generate_text(prompt: str) -> str:
    client = get_client()

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
    )

    return response.text or ""