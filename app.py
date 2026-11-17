from openai import OpenAI
import gradio as gr

from config import ACTOR_MODEL, GEMINI_API_KEY, GEMINI_BASE_URL
from styles import CSS, JS
from system_prompt_builder import build_system_prompt

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url=GEMINI_BASE_URL,
)

SYSTEM_PROMPT = build_system_prompt()


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
    """Normalize Gradio chat history into clean OpenAI-compatible role/content dicts."""
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
    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + _normalize_history(history)
        + [{"role": "user", "content": user_text}]
    )
    response = client.chat.completions.create(model=ACTOR_MODEL, messages=messages)

    return response.choices[0].message.content


if __name__ == "__main__":
    gr.ChatInterface(
        chat,
        title="Digital Twin",
        description="Talk to my AI twin about my career",
        chatbot=gr.Chatbot(show_label=False),
    ).launch(css=CSS, js=JS, theme=gr.themes.Base())
