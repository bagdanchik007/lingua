"""Optional OpenAI provider. Aktiv nur wenn OPENAI_API_KEY gesetzt ist."""
import os
from app.services.llm.base import LLMProvider, LLMMessage, LLMResponse


class OpenAIProvider(LLMProvider):
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def complete(self, messages: list[LLMMessage], **kwargs) -> LLMResponse:
        if not self.api_key:
            return LLMResponse(
                content="[OpenAI] Kein OPENAI_API_KEY gesetzt – bitte Mock nutzen oder Key konfigurieren.",
                provider="openai",
                model=self.model,
            )
        try:
            from openai import OpenAI  # type: ignore

            client = OpenAI(api_key=self.api_key)
            payload = [{"role": m.role, "content": m.content} for m in messages]
            resp = client.chat.completions.create(model=self.model, messages=payload)
            text = resp.choices[0].message.content or ""
            return LLMResponse(content=text, provider="openai", model=self.model)
        except Exception as exc:
            return LLMResponse(
                content=f"[OpenAI Fehler] {exc}",
                provider="openai",
                model=self.model,
            )
