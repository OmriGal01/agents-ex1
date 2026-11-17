from pathlib import Path
from openai import OpenAI

from config import (
    CRITIC_MODEL,
    EVALUATOR_SYSTEM_PROMPT_FILE,
    EVALUATOR_USER_PROMPT_FILE,
    INFO_DOCS_PATH,
)
from evaluator.models import Evaluation
from prompt_builder import build_prompt


class Evaluator:
    def __init__(
        self,
        client: OpenAI,
        model: str = CRITIC_MODEL,
        system_prompt_file: Path = EVALUATOR_SYSTEM_PROMPT_FILE,
        user_prompt_file: Path = EVALUATOR_USER_PROMPT_FILE,
        docs_dir: Path = INFO_DOCS_PATH,
    ) -> None:
        self.client = client
        self.model = model
        self.user_prompt_file = user_prompt_file
        self.system_prompt = build_prompt(
            prompt_file=system_prompt_file,
            docs_dir=docs_dir,
        )

    @staticmethod
    def _format_history(
        conversation_history: list[dict[str, str]] | None
    ) -> str:
        if not conversation_history:
            return "No prior conversation."

        lines: list[str] = []
        for entry in conversation_history:
            role = entry.get("role", "unknown").capitalize()
            content = entry.get("content", "").strip()
            if content:
                lines.append(f"{role}: {content}")

        return "\n".join(lines) if lines else "No prior conversation."

    def evaluate(
        self,
        user_question: str,
        candidate_answer: str,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> Evaluation:

        conv_history_formatted = self._format_history(conversation_history)
        user_prompt = build_prompt(
            self.user_prompt_file,
            conversation_history=conv_history_formatted,
            user_question=user_question,
            candidate_answer=candidate_answer
        )

        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=Evaluation,
        )

        evaluation = response.choices[0].message.parsed
        if evaluation is None:
            raise ValueError("Model returned an empty or unparseable evaluation.")

        return evaluation
