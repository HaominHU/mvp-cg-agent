import os
from dotenv import load_dotenv

from app.models import LLMProvider, OpenAIModel

load_dotenv()

class Settings:
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    DEFAULT_LLM_PROVIDER: str = os.getenv("DEFAULT_LLM_PROVIDER", LLMProvider.OPENAI.value)
    DEFAULT_OPENAI_MODEL: str = os.getenv("DEFAULT_OPENAI_MODEL", OpenAIModel.GPT_5_MINI.value)


settings = Settings()
