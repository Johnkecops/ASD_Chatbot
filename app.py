"""Streamlit interface for APABOT."""

from __future__ import annotations

import streamlit as st

from apabot import APABotEngine
from apabot.config import PAPER_CONFIG


st.set_page_config(page_title="APABOT", page_icon="💬", layout="wide")


@st.cache_resource
def load_engine() -> APABotEngine:
    return APABotEngine()


engine = load_engine()

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
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    result = engine.chat(prompt, st.session_state.messages)
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
