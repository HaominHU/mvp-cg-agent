from openai import OpenAI

from app.config import settings
from app.models import LLMProvider


def call_llm(
    prompt: str,
    provider: str,
    model: str,
) -> str:
    if provider == LLMProvider.OPENAI:
        return call_openai(prompt=prompt, model=model)

    raise ValueError(f"Unsupported provider: {provider}")


def call_openai(prompt: str, model: str) -> str:
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in environment.")

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    response = client.responses.create(
        model=model,
        input=prompt,
    )

    return response.output_text
