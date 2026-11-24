from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMMessage:
    role: str  # system | user | assistant
    content: str


@dataclass
class LLMResponse:
    content: str
    provider: str
    model: str | None = None


class LLMProvider(ABC):
    """Abstraktion für LLM-Anbindung (OpenAI, lokal, Mock)."""

    @abstractmethod
    def complete(self, messages: list[LLMMessage], **kwargs) -> LLMResponse:
        raise NotImplementedError
