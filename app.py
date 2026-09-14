"""Streamlit interface for APABOT."""

from __future__ import annotations

import importlib.util

import streamlit as st

from apabot import APABotEngine
from apabot.config import DEFAULT_MODEL_FILE, PAPER_CONFIG


st.set_page_config(page_title="APABOT", page_icon="💬", layout="wide")


def check_dependencies() -> dict[str, bool]:
    """Cheap presence check (no import) for the two mandatory ML dependencies."""
    return {
        "torch": importlib.util.find_spec("torch") is not None,
        "parlai": importlib.util.find_spec("parlai") is not None,
    }


@st.cache_resource
def load_engine() -> APABotEngine:
    return APABotEngine()


# Dependency/model-status banner — rendered first so it is the first thing a
# visitor sees, above the title. PyTorch and ParlAI are mandatory for the
# trained APABOT model; without them the app only runs the keyword-based
# fallback responder in apabot/engine.py, not the paper's chatbot.
deps = check_dependencies()
missing = [name for name, installed in deps.items() if not installed]
engine = load_engine()

if missing:
    st.error(
        "🚫 Missing mandatory dependency: **"
        + ", ".join(missing)
        + "**. PyTorch and ParlAI are both required to run the trained APABOT model. "
        "Install with `pip install -r requirements.txt`. Until then, every reply below "
        "comes from the limited fallback responder, not the trained model."
    )
elif not engine.is_using_parlai:
    st.warning(
        "⚠️ PyTorch and ParlAI are installed, but no trained model was found at "
        f"`{DEFAULT_MODEL_FILE}`. Replies below use the fallback responder. "
        "Run `python3 scripts/train_parlai.py` to train one."
    )
else:
    st.success("✅ PyTorch and ParlAI are installed and the trained model is active.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello. I’m APABOT, a conversational support prototype inspired by the 2023 paper. "
                "You can ask about ASD, sensory hypersensitivity, or talk through a situation."
            ),
        }
    ]

st.title("APABOT")
st.caption("ASD support chatbot prototype reconstructed from the paper and wrapped in Streamlit.")

with st.sidebar:
    st.subheader("Paper Configuration")
    st.write(f"Framework: `{PAPER_CONFIG['framework']}`")
    st.write(f"Pretrained model: `{PAPER_CONFIG['pretrained_model']}`")
    st.write(f"Tasks: `{', '.join(PAPER_CONFIG['tasks'])}`")
    st.write(f"Learning rate: `{PAPER_CONFIG['learning_rate']}`")
    st.write(f"Warmup updates: `{PAPER_CONFIG['warmup_updates']}`")
    st.write(f"Validation interval: `{PAPER_CONFIG['validation_every_n_epochs']}` epochs")
    st.write(f"Max train time: `{PAPER_CONFIG['max_train_time_seconds']}` seconds")
    st.info(
        "This app is not a medical device. The paper itself recommends further clinical "
        "validation and ethical clearance before real-world patient deployment."
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Type your message")
if prompt:
    history = list(st.session_state.messages)  # turns before this one, matching chat_cli.py's contract
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    result = engine.chat(prompt, history)
    assistant_message = f"{result.response}\n\n`Backend: {result.backend}`"
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    with st.chat_message("assistant"):
        st.markdown(assistant_message)

with st.expander("About this reconstruction"):
    st.markdown(
        """
This implementation follows the paper's published design as closely as the manuscript allows:

- ParlAI is the primary framework.
- The training recipe uses `blended_skill_talk` and `empathetic_dialogues`.
- The pretrained base model is `blender_90M`.
- The reported paper settings include Adam, learning rate `1e-5`, `warmup_updates=100`,
  validation every `0.25` epochs, and maximum training time of `20` minutes.

When a local ParlAI model file is unavailable, the app falls back to a lightweight
supportive responder so the interface remains usable.
"""
    )
