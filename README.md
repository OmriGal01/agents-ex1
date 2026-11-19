# Omri's Digital Career Chatbot (Actor–Critic Architecture)

A grounded personal career chatbot representing **Omri Gal**, built with Python, Gradio, Pydantic, and the OpenAI SDK against Google's Gemini API.  
Every user question passes through a runtime **Actor–Critic** loop: an **Actor** generates a candidate answer grounded in background documents, and a **Critic** evaluates it against strict factual and style criteria using structured Pydantic output (`Evaluation`). Rejected drafts are fed back to the Actor for revision (up to 3 attempts), and all attempts are recorded in a structured JSON execution log.

---

## Requirements & Python Version

- **Python**: `3.12` (tested on Python `3.12`; compatible with Python `3.10+`)
- **Dependencies**: Listed in [`requirements.txt`](./requirements.txt):
  - `openai>=1.50.0`
  - `pydantic>=2.0.0`
  - `gradio>=6.0.0`
  - `python-dotenv>=1.0.0`

---

## Installation

1. **Clone the repository** and enter the project directory:
   ```bash
   git clone <repository-url>
   cd agents-ex1
   ```

2. **Create and activate a virtual environment** (recommended):
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Setup

1. Copy `.env.example` to `.env`:
   - **Windows (PowerShell)**:
     ```powershell
     Copy-Item .env.example .env
     ```
   - **macOS / Linux**:
     ```bash
     cp .env.example .env
     ```

2. Open `.env` and set your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here

   # Optional model overrides (default: gemini-3.5-flash-lite)
   ACTOR_MODEL=
   CRITIC_MODEL=
   ```
   > **Note**: Never commit `.env` to version control (it is excluded via `.gitignore`).

---

## Models & Experiment Configuration

All defaults are defined in [`config.py`](./config.py):

| Setting | Value Used in Experiments |
| :--- | :--- |
| **API Endpoint** | `https://generativelanguage.googleapis.com/v1beta/openai/` (Gemini OpenAI-compatible API) |
| **SDK** | `openai` Python SDK (`chat.completions.create` for Actor; `beta.chat.completions.parse` for Critic) |
| **Actor Model (`ACTOR_MODEL`)** | `gemini-3.5-flash-lite` |
| **Critic Model (`CRITIC_MODEL`)** | `gemini-3.5-flash-lite` |
| **Structured Output Schema** | Pydantic `Evaluation(is_acceptable: bool, feedback: str)` ([`evaluator/models.py`](./evaluator/models.py)) |
| **Max Attempts (`MAX_ATTEMPTS`)** | `3` (1 initial attempt + up to 2 feedback-guided revisions) |
| **Background Sources (`info-docs/`)** | [`omri-summary.md`](./info-docs/omri-summary.md), [`omri-linkedin-cv.md`](./info-docs/omri-linkedin-cv.md) |
| **Prompt Templates (`prompts/`)** | [`actor-system-prompt.md`](./prompts/actor-system-prompt.md), [`actor-revision-prompt.md`](./prompts/actor-revision-prompt.md), [`critic-system-prompt.md`](./prompts/critic-system-prompt.md), [`critic-user-prompt.md`](./prompts/critic-user-prompt.md) |

---

## Running the Chat Application

Start the local Gradio web interface:

```bash
python app.py
```

Open the local URL printed in the terminal (default: `http://127.0.0.1:7860`).  
- The UI supports conversations in both **Hebrew** (automatic RTL alignment) and **English** (LTR alignment).
- Only user messages and final approved responses (or termination notices) are displayed in the chat history.
- All drafts, Critic decisions, and feedback are logged separately to `logs/execution_log.json`.

---

## Running Tests & Part D Scenarios

1. **Logger Unit Tests** (offline, uses a temporary directory):
   ```bash
   python -m unittest tests/test_logger.py -v
   ```

2. **Evaluator Verification Tests** (4 fabricated cases: 2 approved, 2 rejected, with and without conversation history):
   ```bash
   python tests/test_evaluator.py
   ```

3. **Part D — 5-Scenario Experiment Suite** (runs live Scenarios 1–4 + simulated control-flow Scenario 5):
   ```bash
   python tests/run_scenarios.py
   ```
   Running this script generates:
   - Structured JSON execution log: [`logs/scenarios_log.json`](./logs/scenarios_log.json)
   - Formatted Markdown results summary: [`docs/scenarios_results.md`](./docs/scenarios_results.md)

---

## Project Structure

```text
.
├── app.py                        # Gradio ChatInterface entry point
├── config.py                     # Paths, model names, MAX_ATTEMPTS, env loading
├── orchestrator.py               # Actor-Critic retry loop & error handling
├── prompt_builder.py             # Generic cached prompt & document loader
├── logger.py                     # Pydantic execution log models & JSON logger
├── styles.py                     # Gradio IDE dark-mode CSS & RTL/timer JS
├── actor/
│   ├── __init__.py
│   └── actor.py                  # Actor (generator & feedback-driven reviser)
├── evaluator/
│   ├── __init__.py
│   ├── evaluator.py              # Critic (structured Pydantic evaluator)
│   └── models.py                 # Pydantic Evaluation schema
├── prompts/                      # Actor & Critic prompt templates
├── info-docs/                    # Personal summary & LinkedIn/CV background docs
├── tests/
│   ├── test_logger.py            # Unit tests for ExecutionLogger
│   ├── test_evaluator.py         # 4-case manual Critic verification script
│   └── run_scenarios.py          # Registry-based runner for Part D Scenarios 1-5
├── logs/
│   └── scenarios_log.json        # Recorded Part D execution logs
├── docs/
│   ├── architecture.md           # Mermaid system architecture diagram
│   ├── architecture.svg          # Static SVG system architecture diagram
│   └── scenarios_results.md      # Part D experimental results report
├── .env.example                  # Environment variable template (no secrets)
└── requirements.txt              # Python package dependencies
```
