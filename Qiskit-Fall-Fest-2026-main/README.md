# Qiskit Fall Fest 2026 — Challenge Solutions

This repository contains worked solutions for the four challenge sheets supplied with the task.

## Contents
- `challenge1/` — Predict the Output
- `challenge2/` — Make the Quantum Coin Biased
- `challenge3/` — Can You Change the Correlation?
- `challenge4/` — Quantum Correlation Switch

## Setup

Use Python 3.10+ in a virtual environment if possible.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

python -m pip install -r requirements.txt
```

Run a challenge from the repository root, for example:

```bash
python challenge1/solution.py
```

Each script uses Qiskit's local `StatevectorSampler` so it can run without IBM Quantum account credentials. It executes 100 shots per experiment, prints counts, and saves histogram PNGs in the same challenge folder.

## Notes
- Measurement counts are sampled, so results for a superposition circuit can vary from run to run.
- Circuits containing only deterministic X gates should produce deterministic results.
- The explanations and predictions are included in the scripts and can be adapted into your own notebook submission.
- Please run the code yourself, check the output, and make sure you understand each gate before submitting it. Add your own observations from your actual run rather than claiming sample counts are guaranteed.
