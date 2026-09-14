# APABOT

APABOT is a Python and Streamlit reconstruction of the paper **"APABOT: A Chatbot for ASD Treatment Implemented by ParlAI"** from the PDF included in this repository:

- [Shiloputra_et_al___2023___APABOT_A_Chatbot_for_ASD_Treatment_Implemented_by_ParlAI_RINarxiv.pdf](./Shiloputra_et_al___2023___APABOT_A_Chatbot_for_ASD_Treatment_Implemented_by_ParlAI_RINarxiv.pdf)

## What this repository contains

- `apabot/`: core Python package for inference, safety checks, and paper configuration
- `scripts/train_parlai.py`: paper-aligned ParlAI training launcher
- `scripts/chat_cli.py`: terminal chat interface
- `app.py`: Streamlit application
- `LICENSE.txt`: project license

## Paper details translated into code

The manuscript reports the following design:

- Framework: `ParlAI`
- Pretrained model: `blender_90M`
- Datasets/tasks: `blended_skill_talk`, `empathetic_dialogues`
- Optimizer: `Adam`
- Learning rate: `1e-5`
- Warmup updates: `100`
- Validation interval: `0.25` epochs
- Maximum training time: `20` minutes
- Reported hardware: single Tesla T4 GPU

These parameters are captured in [`apabot/config.py`](apabot/config.py).

## Important limitations

- This project is a reconstruction from the PDF, not an official release from the paper authors.
- The paper itself states that further **clinical validation** and **ethical clearance** are required before real-world deployment with ASD patients.
- The included fallback mode is a practical addition for local demos when a trained ParlAI model is unavailable.
- This repository is **not** a medical device and must not be used as a substitute for professional care.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Dependencies

The included [`requirements.txt`](requirements.txt) contains:

```txt
streamlit>=1.45.0
parlai>=1.7.2
torch>=2.2.0
```

**PyTorch and ParlAI are mandatory to run the trained APABOT model — this is not optional.** With
only `streamlit` installed, the app still starts, but every reply comes from a hardcoded
keyword-matching fallback in `apabot/engine.py`, not the paper's model. The Streamlit app checks
both dependencies on load and shows a banner at the top of the page: red if either is missing,
yellow if both are installed but no trained model file exists yet, green once the trained model is
active.

## Run the Streamlit app

```bash
streamlit run app.py
```

## Run the CLI chatbot

```bash
python3 scripts/chat_cli.py
```

## Print the paper-aligned training command

```bash
python3 scripts/train_parlai.py --dry-run
```

## Train the ParlAI model

```bash
python3 scripts/train_parlai.py --model-file models/apabot_model
```

This launches a reconstructed version of the training recipe reported in the paper. Exact reproduction may still differ because the manuscript does not publish every preprocessing and runtime detail.

## Suggested project extensions

- Add persistent conversation logging with consent controls
- Add evaluation scripts for perplexity, token accuracy, and loss
- Add structured prompt templates for ASD-oriented conversational practice
- Add a curated ASD knowledge base reviewed by clinicians
- Add explicit guardrails for crisis handling and referral pathways

## Citation context

If you use this repository academically, please cite the original paper and clearly note that this codebase is a reconstruction based on the PDF description rather than an official upstream implementation.

## AI Disclaimer

This codebase was developed with the assistance of Claude Code. While the AI provided code generation, debugging, and structural support, the human developer maintains full responsibility for reviewing, testing, and maintaining all content and functionality
