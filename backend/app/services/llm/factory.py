import os

from app.services.llm.base import LLMProvider
from app.services.llm.mock_provider import MockLLMProvider


def get_llm_provider() -> LLMProvider:
    """
    Wählt den Provider über ENV:
    LLM_PROVIDER=mock|openai (openai folgt später mit API-Key)
    """
    name = os.getenv("LLM_PROVIDER", "mock").lower()
    if name == "mock":
        return MockLLMProvider()
    # Fallback sicherheitshalber
    return MockLLMProvider()
