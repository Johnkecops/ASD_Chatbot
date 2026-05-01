#!/usr/bin/env python3
"""Simple command-line chat interface for APABOT."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apabot import APABotEngine


def main() -> int:
    engine = APABotEngine()
    history: list[dict[str, str]] = []

    print("APABOT CLI")
    print("Type 'quit' to exit.\n")
    while True:
        user_message = input("You: ").strip()
        if user_message.lower() in {"quit", "exit"}:
            break

        result = engine.chat(user_message, history)
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": result.response})

        print(f"APABOT [{result.backend}]: {result.response}")
        print(f"Note: {result.note}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
