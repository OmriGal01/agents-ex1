import sys
from pathlib import Path

# Allow running directly as `python tests/test_evaluator.py`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import critic

TEST_CASES = [
    {
        "name": "1. Approved (No conversation history)",
        "history": None,
        "question": "Where does Omri study and what is his GPA?",
        "candidate_answer": (
            "Omri Gal is a third-year Computer Science honors student at Reichman "
            "University in the accelerated B.Sc./M.Sc. program. He holds a 99 GPA "
            "and is ranked 1st in his class on the Dean's List."
        ),
        "expected_acceptable": True,
    },
    {
        "name": "2. Approved (With conversation history)",
        "history": [
            {
                "role": "user",
                "content": "Where did Omri intern in Summer 2026?",
            },
            {
                "role": "assistant",
                "content": (
                    "Omri worked as an AI Tools Developer Intern at Mad Brain Games "
                    "during Summer 2026."
                ),
            },
        ],
        "question": "What did he build there?",
        "candidate_answer": (
            "During his internship at Mad Brain Games, Omri architected and deployed "
            "a modular Python competitive-intelligence AI agent with CLI and FastAPI "
            "interfaces, a dynamic skill registry, and pluggable LLM adapters. He also "
            "built asynchronous data collection pipelines with strict Pydantic validation "
            "and automated report delivery via a website and Telegram webhooks."
        ),
        "expected_acceptable": True,
    },
    {
        "name": "3. Rejected (No conversation history - fabricated hobby)",
        "history": None,
        "question": "What hobbies does Omri have outside of software engineering?",
        "candidate_answer": (
            "Omri is a hobbyist woodworker who builds functional furniture like a "
            "10-seater poker table, and he is also an avid marathon runner who won "
            "the Tel Aviv Marathon in 2025."
        ),
        "expected_acceptable": False,
    },
    {
        "name": "4. Rejected (With conversation history - fabricated tech stack)",
        "history": [
            {
                "role": "user",
                "content": "Tell me about Omri's AI-Powered Grocery List Manager project.",
            },
            {
                "role": "assistant",
                "content": (
                    "Omri built the AI-Powered Grocery List Manager as a cloud-native "
                    "Telegram bot using a FastAPI backend, Cloud SQL (PostgreSQL), and "
                    "an MCP server deployed on Google Cloud Run."
                ),
            },
        ],
        "question": "Which cloud provider and database did he use for that project?",
        "candidate_answer": (
            "For the AI-Powered Grocery List Manager, Omri deployed the backend on "
            "AWS Lambda and used MongoDB Atlas as the database."
        ),
        "expected_acceptable": False,
    },
]


def run_evaluator_tests() -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    passed = 0
    for case in TEST_CASES:
        print(f"=== {case['name']} ===")
        evaluation = critic.evaluate(
            user_question=case["question"],
            candidate_answer=case["candidate_answer"],
            conversation_history=case["history"],
        )
        matched = evaluation.is_acceptable == case["expected_acceptable"]
        status = "PASS" if matched else "FAIL"
        if matched:
            passed += 1

        print(f"Expected is_acceptable: {case['expected_acceptable']}")
        print(f"Actual is_acceptable:   {evaluation.is_acceptable} [{status}]")
        print(f"Feedback: {evaluation.feedback}\n")

    print(f"Summary: {passed}/{len(TEST_CASES)} tests matched expectations.")
    if passed != len(TEST_CASES):
        sys.exit(1)


if __name__ == "__main__":
    run_evaluator_tests()
