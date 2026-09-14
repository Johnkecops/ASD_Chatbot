"""Safety rules for a non-clinical ASD support chatbot."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class SafetyResult:
    allowed: bool
    response: str | None = None
    reason: str | None = None


CRISIS_TERMS = {
    "suicide",
    "kill myself",
    "hurt myself",
    "self harm",
    "self-harm",
    "want to die",
    "end my life",
}

# Word-boundary match: plain substring search false-triggers on e.g. "myself
# harmless" (contains "self harm") and misses nothing a substring check would
# have caught, since every term already reads as whole words.
_CRISIS_PATTERNS = [re.compile(r"\b" + re.escape(term) + r"\b") for term in CRISIS_TERMS]


def screen_message(message: str) -> SafetyResult:
    lowered = message.lower()
    for pattern in _CRISIS_PATTERNS:
        if pattern.search(lowered):
            return SafetyResult(
                allowed=False,
                reason="crisis",
                response=(
                    "I’m not able to help with immediate crisis care. Please contact local "
                    "emergency services or a licensed mental health professional right now. "
                    "If you are in the United States or Canada, call or text 988."
                ),
            )
    return SafetyResult(allowed=True)


def add_supportive_suffix(response: str) -> str:
    suffix = (
        " If you want, we can keep the conversation simple and take one question at a time."
    )
    if response.endswith(suffix):
        return response
    return f"{response}{suffix}"
