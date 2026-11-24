from app.services.llm.base import LLMProvider, LLMMessage, LLMResponse


class MockLLMProvider(LLMProvider):
    """Deterministischer Platzhalter – ohne externe API."""

    def complete(self, messages: list[LLMMessage], **kwargs) -> LLMResponse:
        user_msgs = [m.content for m in messages if m.role == "user"]
        last = user_msgs[-1] if user_msgs else ""
        mode = kwargs.get("mode", "free")
        lang = kwargs.get("language_code", "de")

        if mode == "correction":
            content = (
                f"[Mock-Korrektur] Zu deinem Text auf '{lang}':\n"
                f"„{last}“\n"
                "Vorschlag: Formuliere den Satz mit korrektem Artikel und Verbzweitstellung."
            )
        elif mode == "roleplay":
            content = (
                f"[Mock-Rollenspiel] Ich bleibe in der Rolle.\n"
                f"Du sagtest: „{last}“\n"
                "Antwort: Das klingt gut – erzähl mir bitte noch mehr Details."
            )
        else:
            content = (
                f"[Mock-KI/{lang}] Danke für deine Nachricht: „{last[:120]}“. "
                "Hier würde das echte Modell antworten. "
                "Tipp: Achte auf Wortstellung und Zeitform."
            )
        return LLMResponse(content=content, provider="mock", model="mock-v1")
