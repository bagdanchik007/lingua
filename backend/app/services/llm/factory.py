import os

from app.services.llm.base import LLMProvider
from app.services.llm.mock_provider import MockLLMProvider


def get_llm_provider() -> LLMProvider:
    name = os.getenv("LLM_PROVIDER", "mock").lower()
    if name == "openai":
        from app.services.llm.openai_provider import OpenAIProvider

        return OpenAIProvider()
    return MockLLMProvider()
