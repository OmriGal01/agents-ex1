import json
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import actor, critic
from config import ACTOR_MODEL, BASE_DIR, CRITIC_MODEL, LOGS_PATH, MAX_ATTEMPTS
from evaluator.models import Evaluation
from logger import ExecutionLogger
from orchestrator import ChatOrchestrator, format_max_attempts_message

SCENARIOS_LOG_FILE = LOGS_PATH / "scenarios_log.json"
SCENARIOS_REPORT_FILE = BASE_DIR / "docs" / "scenarios_results.md"


class MockAlwaysRejectEvaluator:
    """Simulated Critic used strictly for Scenario 5 control-flow testing."""

    def evaluate(
        self,
        user_question: str,
        candidate_answer: str,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> Evaluation:
        return Evaluation(
            is_acceptable=False,
            feedback=(
                "[Mock Evaluator — Control-Flow Test] Simulated rejection to verify "
                "max-attempts termination after 3 failed attempts."
            ),
        )


@dataclass
class ScenarioTurn:
    log_id: str
    question: str
    displayed_output: str
    history_summary: str | None = None
    injected_first_draft: str | None = None


@dataclass
class ScenarioResult:
    title: str
    expected: str
    matched: bool
    turns: list[ScenarioTurn]
    is_mock: bool = False
    source_reference: str | None = None


@dataclass
class ScenarioContext:
    live_orchestrator: ChatOrchestrator
    mock_orchestrator: ChatOrchestrator
    log_file: Path = field(default=SCENARIOS_LOG_FILE)

    def load_logs(self) -> list[dict]:
        return json.loads(self.log_file.read_text(encoding="utf-8")) if self.log_file.exists() else []

    def run_turn(
        self,
        log_id: str,
        question: str,
        history: list[dict[str, str]] | None = None,
        injected_first_draft: str | None = None,
        use_mock: bool = False,
        history_summary: str | None = None,
    ) -> tuple[ScenarioTurn, dict]:
        orch = self.mock_orchestrator if use_mock else self.live_orchestrator
        output = orch.run(
            question,
            conversation_history=history or [],
            scenario_id=log_id,
            injected_first_draft=injected_first_draft,
        )
        turn = ScenarioTurn(
            log_id=log_id,
            question=question,
            displayed_output=output,
            history_summary=history_summary,
            injected_first_draft=injected_first_draft,
        )
        return turn, self.load_logs()[-1]


ScenarioRunner = Callable[[ScenarioContext], ScenarioResult]
SCENARIO_REGISTRY: list[ScenarioRunner] = []


def register_scenario(
    title: str,
    expected: str,
    *,
    is_mock: bool = False,
    source_reference: str | None = None,
) -> Callable[[Callable[[ScenarioContext], tuple[bool, list[ScenarioTurn]]]], ScenarioRunner]:
    def decorator(
        func: Callable[[ScenarioContext], tuple[bool, list[ScenarioTurn]]],
    ) -> ScenarioRunner:
        def wrapped(ctx: ScenarioContext) -> ScenarioResult:
            matched, turns = func(ctx)
            return ScenarioResult(
                title=title,
                expected=expected,
                matched=matched,
                turns=turns,
                is_mock=is_mock,
                source_reference=source_reference,
            )

        wrapped.__name__ = func.__name__
        SCENARIO_REGISTRY.append(wrapped)
        return wrapped

    return decorator


@register_scenario(
    title="Scenario 1 — Question on Existing Information",
    expected="Approved Hebrew answer citing Reichman University, 99 GPA, and accelerated B.Sc./M.Sc. honors program.",
    source_reference="`info-docs/omri-summary.md` & `info-docs/omri-linkedin-cv.md` (Education section: Reichman University, GPA 99, 1st in class, Honors).",
)
def scenario_1_existing_info(ctx: ScenarioContext) -> tuple[bool, list[ScenarioTurn]]:
    turn, log = ctx.run_turn(
        "scenario_1",
        "היכן עומרי לומד, מה ממוצע הציונים שלו ובאיזו תוכנית הוא נמצא?",
    )
    matched = log["final_status"] == "approved" and "99" in turn.displayed_output and "רייכמן" in turn.displayed_output
    return matched, [turn]


@register_scenario(
    title="Scenario 2 — Follow-up Question",
    expected="Turn 1 identifies Mad Brain Games; Turn 2 resolves 'there' from history and describes the scalable skill plugin architecture challenge.",
)
def scenario_2_followup(ctx: ScenarioContext) -> tuple[bool, list[ScenarioTurn]]:
    t1, log1 = ctx.run_turn("scenario_2_turn_1", "היכן עומרי עשה את ההתמחות שלו בקיץ 2026?")
    history = [
        {"role": "user", "content": t1.question},
        {"role": "assistant", "content": t1.displayed_output},
    ]
    t2, log2 = ctx.run_turn(
        "scenario_2_turn_2",
        "מה היה האתגר הטכני האהוב עליו שם?",
        history=history,
        history_summary="Includes Turn 1 user question and assistant response.",
    )
    matched = (
        log1["final_status"] == "approved"
        and log2["final_status"] == "approved"
        and "Mad Brain Games" in t1.displayed_output
        and any(k in t2.displayed_output.lower() for k in ("תוספים", "plugin", "סקיילביל"))
    )
    return matched, [t1, t2]


@register_scenario(
    title="Scenario 3 — Missing Information",
    expected="Explicitly states that background sources lack Omri's high school and major without inventing facts; approved by Critic.",
)
def scenario_3_missing_info(ctx: ScenarioContext) -> tuple[bool, list[ScenarioTurn]]:
    turn, log = ctx.run_turn("scenario_3", "באיזה תיכון עומרי למד ומה הייתה המגמה שלו בבגרות?")
    matched = log["final_status"] == "approved" and any(
        w in turn.displayed_output for w in ("אין", "לא מופיע", "חסר", "אינו")
    )
    return matched, [turn]


@register_scenario(
    title="Scenario 4 — Rejection & Revision",
    expected="Attempt 1 (injected flawed draft with invented marathon win & piano) is rejected by Critic; Attempt 2 is revised by Actor and approved.",
)
def scenario_4_rejection_and_revision(ctx: ScenarioContext) -> tuple[bool, list[ScenarioTurn]]:
    flawed_draft = (
        "עומרי פיתח את ה-AI-Powered Grocery List Manager. "
        "בתחום התחביבים, הוא עוסק בנגרות, וגם זכה במקום הראשון במרתון תל אביב 2025 "
        "ומנגן על פסנתר באופן מקצועי."
    )
    turn, log = ctx.run_turn(
        "scenario_4",
        "אילו פרויקטים אישיים עומרי פיתח ומה התחביבים שלו?",
        injected_first_draft=flawed_draft,
    )
    attempts = log["attempts"]
    matched = (
        len(attempts) >= 2
        and attempts[0]["evaluator_decision"] == "rejected"
        and log["final_status"] == "approved"
        and "מרתון" not in turn.displayed_output
        and "פסנתר" not in turn.displayed_output
    )
    return matched, [turn]


@register_scenario(
    title="Scenario 5 — Max Attempts Exhausted (Mock Control-Flow Test)",
    expected="All 3 attempts are rejected by MockAlwaysRejectEvaluator; stops after Attempt 3 and displays limit notice without showing rejected drafts.",
    is_mock=True,
)
def scenario_5_max_attempts_mock(ctx: ScenarioContext) -> tuple[bool, list[ScenarioTurn]]:
    turn, log = ctx.run_turn(
        "scenario_5_mock_control_flow",
        "באילו שפות תכנות עומרי שולט?",
        use_mock=True,
    )
    attempts = log["attempts"]
    matched = (
        len(attempts) == MAX_ATTEMPTS
        and all(a["evaluator_decision"] == "rejected" for a in attempts)
        and log["final_status"] == "max_attempts_exceeded"
        and turn.displayed_output == format_max_attempts_message(MAX_ATTEMPTS)
    )
    return matched, [turn]


def _render_scenario(res: ScenarioResult, logs_by_id: dict[str, dict]) -> list[str]:
    match_label = "Yes" if res.matched else "No"
    lines = [
        f"### {res.title}",
        f"- **Scenario ID(s)**: `{', '.join(t.log_id for t in res.turns)}`",
        f"- **Expected**: {res.expected}",
        f"- **Matched Expectation**: **{match_label}**",
    ]
    if res.source_reference:
        lines.append(f"- **Supporting Source**: {res.source_reference}")
    lines.append("")

    for turn in res.turns:
        entry = logs_by_id.get(turn.log_id, {})
        lines.append(f"#### Turn (`{turn.log_id}`)")
        if turn.history_summary:
            lines.append(f"- **Prior History**: {turn.history_summary}")
        lines.append(f"- **User Question**: {turn.question}")
        if turn.injected_first_draft:
            lines.append(f"- **Injected Flawed Draft**: {turn.injected_first_draft}")
        lines.append(f"- **Final Status**: `{entry.get('final_status', 'unknown')}`")
        lines.append(f"- **Displayed Output**:\n\n> {turn.displayed_output}\n")
        lines.append("**Attempt Log**:")
        for att in entry.get("attempts", []):
            lines.append(
                f"- **Attempt {att['attempt_number']}** (`{att['evaluator_decision']}`)\n"
                f"  - **Candidate**: {att['candidate_answer']}\n"
                f"  - **Feedback**: {att['feedback']}"
            )
        lines.append("")

    return lines + ["---", ""]


def write_markdown_report(results: list[ScenarioResult], log_entries: list[dict]) -> None:
    logs_by_id = {e["scenario_id"]: e for e in log_entries}
    lines = [
        "# Part D — Scenarios & Experimental Results",
        "",
        f"- **Actor Model**: `{ACTOR_MODEL}` | **Critic Model**: `{CRITIC_MODEL}` | **Max Attempts**: `{MAX_ATTEMPTS}`",
        "- **Raw Execution Log**: [`logs/scenarios_log.json`](../logs/scenarios_log.json)",
        "",
        "---",
        "",
        "## Section A — Live LLM Scenarios (Scenarios 1–4)",
        "",
    ]
    for res in (r for r in results if not r.is_mock):
        lines.extend(_render_scenario(res, logs_by_id))

    lines.extend(
        [
            "## Section B — Simulated Control-Flow Test (Scenario 5 — Mock Critic)",
            "",
            "> **Note**: Uses `MockAlwaysRejectEvaluator` to verify 3-attempt termination. "
            "Presented separately from live LLM scenarios above.",
            "",
        ]
    )
    for res in (r for r in results if r.is_mock):
        lines.extend(_render_scenario(res, logs_by_id))

    SCENARIOS_REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    SCENARIOS_REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")


def run_all_scenarios() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    if SCENARIOS_LOG_FILE.exists():
        SCENARIOS_LOG_FILE.unlink()

    scenario_logger = ExecutionLogger(log_file=SCENARIOS_LOG_FILE)
    ctx = ScenarioContext(
        live_orchestrator=ChatOrchestrator(actor=actor, evaluator=critic, logger=scenario_logger),
        mock_orchestrator=ChatOrchestrator(
            actor=actor, evaluator=MockAlwaysRejectEvaluator(), logger=scenario_logger
        ),
    )

    results = []
    for scenario_fn in SCENARIO_REGISTRY:
        print(f"Running {scenario_fn.__name__}...")
        results.append(scenario_fn(ctx))

    write_markdown_report(results, ctx.load_logs())

    passed = sum(r.matched for r in results)
    print("\n=== Scenario Execution Summary ===")
    for r in results:
        print(f"[{'PASS' if r.matched else 'FAIL'}] {r.title}")
    print(f"\nPassed: {passed}/{len(results)}")
    print(f"JSON Log: {SCENARIOS_LOG_FILE}\nMarkdown Report: {SCENARIOS_REPORT_FILE}")

    if passed != len(results):
        sys.exit(1)


if __name__ == "__main__":
    run_all_scenarios()
