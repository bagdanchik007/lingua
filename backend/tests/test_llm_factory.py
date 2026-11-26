import os
from app.services.llm.factory import get_llm_provider
from app.services.llm.mock_provider import MockLLMProvider


def test_default_provider_is_mock():
    os.environ.pop("LLM_PROVIDER", None)
    provider = get_llm_provider()
    assert isinstance(provider, MockLLMProvider)


def test_mock_complete():
    provider = MockLLMProvider()
    from app.services.llm.base import LLMMessage

    resp = provider.complete([LLMMessage(role="user", content="Hallo")])
    assert resp.provider == "mock"
    assert len(resp.content) > 0
