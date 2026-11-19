# System Architecture — Actor-Critic Career Chatbot

This diagram illustrates the end-to-end execution flow of the Actor-Critic chatbot (`app.py`, `orchestrator.py`, `actor/`, `evaluator/`, `prompt_builder.py`, and `logger.py`), including the background sources, conversation history, structured `Evaluation` output, the feedback revision loop, and all three exit paths (**Approved**, **Max Attempts Exceeded**, and **Technical Error**).

## Rendered Diagram (Static SVG)

![System Architecture Diagram](./architecture.svg)

## Mermaid Source

```mermaid
flowchart TD
    DOCS["Background Sources<br/>(info-docs/: omri-summary.md,<br/>omri-linkedin-cv.md)"]
    PB["Prompt Builder<br/>(prompt_builder.py)"]
    UI["Gradio Chat UI &amp; History<br/>(app.py)"]
    ORCH["ChatOrchestrator<br/>(orchestrator.py)<br/>attempt = 1 .. 3"]
    ACTOR["Actor (Generator)<br/>(actor/actor.py)<br/>actor-system-prompt.md"]
    CRITIC["Critic (Evaluator)<br/>(evaluator/evaluator.py)<br/>critic-system-prompt.md +<br/>critic-user-prompt.md"]
    EVAL["Structured Output<br/>Pydantic Evaluation<br/>(is_acceptable: bool, feedback: str)"]
    DEC{"is_acceptable?"}
    RETRY{"attempt &lt; 3?"}
    LOG["ExecutionLogger<br/>(logger.py -&gt; logs/execution_log.json)"]

    EXIT_OK["EXIT 1: Approved<br/>final_status = 'approved'<br/>Display answer &amp; update chat history"]
    EXIT_MAX["EXIT 2: Max Attempts Exceeded<br/>final_status = 'max_attempts_exceeded'<br/>Display limit notice (no rejected draft shown)"]
    EXIT_ERR["EXIT 3: Technical Error<br/>evaluator_decision = 'evaluation_not_completed'<br/>final_status = 'technical_error'<br/>Display error notice"]

    DOCS --> PB
    PB -->|"Injected background docs"| ACTOR
    PB -->|"Injected background docs"| CRITIC

    UI -->|"User question +<br/>normalized history"| ORCH
    ORCH -->|"Question + history"| ACTOR
    ACTOR -->|"Candidate draft"| CRITIC
    CRITIC -->|"Parse &amp; validate"| EVAL

    ACTOR -.->|"API / empty response error"| EXIT_ERR
    CRITIC -.->|"API / schema validation error"| EXIT_ERR

    EVAL --> DEC
    DEC -->|"Yes (True)"| EXIT_OK
    DEC -->|"No (False)"| RETRY

    RETRY -->|"Yes: Feedback Loop<br/>(rejected draft + Critic feedback<br/>via actor-revision-prompt.md;<br/>attempt += 1)"| ACTOR
    RETRY -->|"No (attempt == 3)"| EXIT_MAX

    EXIT_OK --> LOG
    EXIT_MAX --> LOG
    EXIT_ERR --> LOG

    EXIT_OK -->|"Approved answer"| UI
    EXIT_MAX -->|"Max attempts message"| UI
    EXIT_ERR -->|"Error message"| UI

    style EXIT_OK fill:#1e4620,stroke:#4caf50,color:#ffffff
    style EXIT_MAX fill:#5c3d0e,stroke:#ff9800,color:#ffffff
    style EXIT_ERR fill:#5c1919,stroke:#f44336,color:#ffffff
    style DOCS fill:#263238,stroke:#607d8b,color:#ffffff
    style UI fill:#1d3557,stroke:#3574f0,color:#ffffff
    style ACTOR fill:#2b2d30,stroke:#3574f0,color:#ffffff
    style CRITIC fill:#2b2d30,stroke:#3574f0,color:#ffffff
    style EVAL fill:#2b2d30,stroke:#4a85f6,color:#ffffff
    style LOG fill:#26282c,stroke:#9397a1,color:#ffffff
```
