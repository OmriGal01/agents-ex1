import gradio as gr
from openai import OpenAI

from actor import Actor
from config import GEMINI_API_KEY, GEMINI_BASE_URL
from evaluator import Evaluator
from orchestrator import ChatOrchestrator
from styles import CSS, JS

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url=GEMINI_BASE_URL,
)

actor = Actor(client)
critic = Evaluator(client)
orchestrator = ChatOrchestrator(actor, critic)


def _extract_text(content) -> str:
    """Extract plain text from a Gradio message content value."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
        return "\n".join(parts)
    return str(content or "")


def _normalize_history(history) -> list[dict[str, str]]:
    """Normalize Gradio chat history into OpenAI-compatible role/content dicts."""
    normalized: list[dict[str, str]] = []
    for entry in history or []:
        if isinstance(entry, dict):
            role = entry.get("role")
            text = _extract_text(entry.get("content"))
            if role in ("user", "assistant") and text:
                normalized.append({"role": role, "content": text})
        elif isinstance(entry, (list, tuple)) and len(entry) == 2:
            user_msg, bot_msg = entry
            if user_msg:
                normalized.append({"role": "user", "content": _extract_text(user_msg)})
            if bot_msg:
                normalized.append({"role": "assistant", "content": _extract_text(bot_msg)})
    return normalized


def chat(message, history):
    user_text = _extract_text(message)
    normalized_history = _normalize_history(history)
    return orchestrator.run(user_text, normalized_history)


if __name__ == "__main__":
    gr.ChatInterface(
        chat,
        title="Digital Twin",
        description="Talk to my AI twin about my career",
        chatbot=gr.Chatbot(show_label=False),
    ).launch(css=CSS, js=JS, theme=gr.themes.Base())
