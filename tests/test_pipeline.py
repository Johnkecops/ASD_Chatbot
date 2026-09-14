"""Regression checks for the caveman-review bug fixes (2026-09-14).

No framework, no fixtures: plain asserts, run with `python3 tests/test_pipeline.py`.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apabot.engine import APABotEngine
from apabot.safety import screen_message


def test_crisis_word_boundary_no_false_positive() -> None:
    # "myself harmless" contains "self harm" as a bare substring; must not trigger.
    assert screen_message("that sounds myself harmless, don't worry").allowed


def test_crisis_word_boundary_still_detects_real_phrase() -> None:
    assert not screen_message("I want to hurt myself").allowed


def test_asd_disclosure_word_boundary_no_false_positive() -> None:
    engine = APABotEngine.__new__(APABotEngine)  # skip __init__, avoid ParlAI probing
    reply = engine._chat_with_fallback("i have asdf, not sure what to do", [])
    assert "Thank you for telling me that" not in reply


def test_asd_disclosure_still_detected() -> None:
    engine = APABotEngine.__new__(APABotEngine)
    reply = engine._chat_with_fallback("i have asd and wanted you to know", [])
    assert "Thank you for telling me that" in reply


def test_is_using_parlai_matches_dependency_availability() -> None:
    # Ties APABotEngine.is_using_parlai (surfaced in app.py's dashboard banner)
    # to reality: without parlai importable, the engine must report fallback.
    import importlib.util

    if importlib.util.find_spec("parlai") is not None:
        return  # this environment has parlai; nothing to assert here
    engine = APABotEngine()
    assert not engine.is_using_parlai


if __name__ == "__main__":
    test_crisis_word_boundary_no_false_positive()
    test_crisis_word_boundary_still_detects_real_phrase()
    test_asd_disclosure_word_boundary_no_false_positive()
    test_asd_disclosure_still_detected()
    test_is_using_parlai_matches_dependency_availability()
    print("All regression checks passed.")
