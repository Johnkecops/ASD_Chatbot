"""Inference engine for APABOT."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import DEFAULT_MODEL_FILE
from .knowledge_base import ASD_KNOWLEDGE, FAQ_PATTERNS
from .safety import add_supportive_suffix, screen_message


@dataclass
class ChatResult:
    response: str
    backend: str
    note: str


class APABotEngine:
    """Use a ParlAI model when available, otherwise a safe fallback responder."""

    def __init__(self, model_file: str | Path | None = None) -> None:
        self.model_file = Path(model_file) if model_file else DEFAULT_MODEL_FILE
        self._parlai_agent = None
        self._parlai_error = None
        self._try_load_parlai()

    def _try_load_parlai(self) -> None:
        try:
            from parlai.core.agents import create_agent_from_model_file
        except Exception as exc:  # pragma: no cover
            self._parlai_error = f"ParlAI import failed: {exc}"
            return

        if not self.model_file.exists():
            self._parlai_error = f"Model file not found: {self.model_file}"
            return

        try:
            self._parlai_agent = create_agent_from_model_file(str(self.model_file), interactive_mode=True)
        except Exception as exc:  # pragma: no cover
            self._parlai_error = f"ParlAI model load failed: {exc}"

    def chat(self, message: str, history: list[dict[str, str]] | None = None) -> ChatResult:
        safety = screen_message(message)
        if not safety.allowed:
            return ChatResult(
                response=safety.response or "Please seek immediate help.",
                backend="safety",
                note="Crisis language detected.",
            )

        if self._parlai_agent is not None:
            try:
                return self._chat_with_parlai(message)
            except Exception as exc:  # pragma: no cover
                self._parlai_error = f"Runtime error while generating from ParlAI: {exc}"

        fallback_response = self._chat_with_fallback(message, history or [])
        return ChatResult(
            response=add_supportive_suffix(fallback_response),
            backend="fallback",
            note=self._parlai_error or "Using local fallback assistant.",
        )

    def _chat_with_parlai(self, message: str) -> ChatResult:
        assert self._parlai_agent is not None
        self._parlai_agent.observe({"text": message, "episode_done": True})
        reply: dict[str, Any] = self._parlai_agent.act()
        text = str(reply.get("text", "")).strip() or "I’m here with you. Could you tell me a bit more?"
        return ChatResult(
            response=add_supportive_suffix(text),
            backend="parlai",
            note="Response generated with a fine-tuned ParlAI model.",
        )

    def _chat_with_fallback(self, message: str, history: list[dict[str, str]]) -> str:
        lowered = message.lower().strip()

        for pattern, key in FAQ_PATTERNS.items():
            if pattern in lowered:
                return ASD_KNOWLEDGE[key]

        if any(token in lowered for token in {"anxious", "afraid", "scared", "overwhelmed", "stressed"}):
            return (
                "That sounds overwhelming. We can slow down together. "
                "Would it help to describe what happened, what you felt, or what support you need right now?"
            )

        if any(token in lowered for token in {"hello", "hi", "hey"}):
            return (
                "Hello. I’m APABOT, a conversational support prototype inspired by the paper. "
                "You can ask about ASD, sensory sensitivity, or talk through how you are feeling."
            )

        if "i have asd" in lowered or "i am autistic" in lowered:
            return (
                "Thank you for telling me that. I’ll try to keep my responses clear and calm. "
                "If you want, we can focus on sensory concerns, communication practice, or a specific situation."
            )

        if lowered.endswith("?"):
            return (
                "I may not have a perfect answer, but I can help think it through. "
                "If your question is about ASD support, sensory sensitivity, or communication, tell me a little more."
            )

        if history:
            return (
                "I’m listening. It sounds like this matters to you. "
                "Can you tell me what part feels hardest right now?"
            )

        return (
            "I’m here to support a calm, simple conversation. "
            "You can ask me about ASD, sensory hypersensitivity, or describe what you are experiencing."
        )
