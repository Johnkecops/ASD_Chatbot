#!/usr/bin/env python3
"""
Module: APABOT ParlAI training launcher
Purpose: Reconstruct the training configuration reported in the APABOT paper
Author: OpenAI Codex for Dr. Arli Aditya Parikesit's project
Date: 2026-05-01
Parameters:
    --model-file: Output path for the fine-tuned model
    --dry-run: Print the training command without executing it
References:
    - Roller et al. 2020. Recipes for building an open-domain chatbot.
    - Miller et al. 2017. ParlAI: A Dialog Research Software Platform.
"""

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apabot.config import DEFAULT_MODEL_FILE, PAPER_CONFIG


def build_train_command(model_file: Path) -> list[str]:
    return [
        "python3",
        "-m",
        "parlai.scripts.train_model",
        "--task",
        ",".join(PAPER_CONFIG["tasks"]),
        "--model",
        "transformer/generator",
        "--init-model",
        PAPER_CONFIG["pretrained_model"],
        "--model-file",
        str(model_file),
        "--optimizer",
        PAPER_CONFIG["optimizer"],
        "--learningrate",
        str(PAPER_CONFIG["learning_rate"]),
        "--warmup_updates",
        str(PAPER_CONFIG["warmup_updates"]),
        "--validation-every-n-epochs",
        str(PAPER_CONFIG["validation_every_n_epochs"]),
        "--max_train_time",
        str(PAPER_CONFIG["max_train_time_seconds"]),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Train APABOT with a paper-aligned ParlAI recipe.")
    parser.add_argument("--model-file", default=str(DEFAULT_MODEL_FILE), help="Path to save the trained model.")
    parser.add_argument("--dry-run", action="store_true", help="Only print the generated command.")
    args = parser.parse_args()

    model_file = Path(args.model_file)
    model_file.parent.mkdir(parents=True, exist_ok=True)

    command = build_train_command(model_file)
    print("Paper-aligned APABOT training command:")
    print(" ".join(shlex.quote(part) for part in command))

    if args.dry_run:
        return 0

    try:
        return subprocess.call(command, cwd=ROOT)
    except FileNotFoundError:
        print("ParlAI is not installed in this environment. Install requirements first.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
