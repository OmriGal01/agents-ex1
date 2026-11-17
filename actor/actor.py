from pathlib import Path
from openai import OpenAI

from config import (
    ACTOR_MODEL,
    ACTOR_REVISION_PROMPT_FILE,
    ACTOR_SYSTEM_PROMPT_FILE,
    INFO_DOCS_PATH,
)
from prompt_builder import build_prompt


class Actor:
    def __init__(
        self,
        client: OpenAI,
        model: str = ACTOR_MODEL,
        system_prompt_file: Path = ACTOR_SYSTEM_PROMPT_FILE,
        revision_prompt_file: Path = ACTOR_REVISION_PROMPT_FILE,
        docs_dir: Path = INFO_DOCS_PATH,
    ) -> None:
        self.client = client
        self.model = model
        self.revision_prompt_file = revision_prompt_file
        self.system_prompt = build_prompt(
            prompt_file=system_prompt_file,
            docs_dir=docs_dir,
        )

    def _build_messages(
        self,
        user_question: str,
        conversation_history: list[dict[str, str]] | None = None,
        rejected_answer: str | None = None,
        critic_feedback: str | None = None,
    ) -> list[dict[str, str]]:

        messages = [{"role": "system", "content": self.system_prompt}]
        messages += conversation_history or []
        messages.append({"role": "user", "content": user_question})
        if rejected_answer and critic_feedback:
            revision_prompt = build_prompt(
                self.revision_prompt_file,
                rejected_answer=rejected_answer,
                critic_feedback=critic_feedback
            )
            messages.append({"role": "user", "content": revision_prompt})

        return messages


    def generate(
        self,
        user_question: str,
        conversation_history: list[dict[str, str]] | None = None,
        rejected_answer: str | None = None,
        critic_feedback: str | None = None,
    ) -> str:

        messages = self._build_messages(
            user_question,
            conversation_history,
            rejected_answer,
            critic_feedback
        )
        response = self.client.chat.completions.create(model=self.model, messages=messages)
        content = response.choices[0].message.content

        if not content:
            raise ValueError("Actor returned an empty response.")

        return content
