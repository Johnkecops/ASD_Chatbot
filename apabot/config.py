"""Configuration values reconstructed from the APABOT paper."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "models"
DEFAULT_MODEL_FILE = MODEL_DIR / "apabot_model"

PAPER_CONFIG = {
    "framework": "ParlAI",
    "pretrained_model": "zoo:blender/blender_90M/model",
    "tasks": ["blended_skill_talk", "empathetic_dialogues"],
    "optimizer": "adam",
    "learning_rate": 1e-5,
    "warmup_updates": 100,
    "validation_every_n_epochs": 0.25,
    "max_train_time_seconds": 20 * 60,
    "reported_steps": 3479,
    "reported_hardware": "single Tesla T4 GPU",
    "notes": (
        "This configuration is reconstructed from the manuscript. "
        "Clinical validation and ethical clearance remain necessary."
    ),
}
