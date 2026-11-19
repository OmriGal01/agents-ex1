import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
PROMPTS_PATH = BASE_DIR / "prompts"
INFO_DOCS_PATH = BASE_DIR / "info-docs"

ACTOR_SYSTEM_PROMPT_FILE = PROMPTS_PATH / "actor-system-prompt.md"
ACTOR_REVISION_PROMPT_FILE = PROMPTS_PATH / "actor-revision-prompt.md"
CRITIC_SYSTEM_PROMPT_FILE = PROMPTS_PATH / "critic-system-prompt.md"
CRITIC_USER_PROMPT_FILE = PROMPTS_PATH / "critic-user-prompt.md"

LOGS_PATH = BASE_DIR / "logs"
EXECUTION_LOG_FILE = LOGS_PATH / "execution_log.json"

MAX_ATTEMPTS = 3

GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY") or "").strip()
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
DEFAULT_MODEL = "gemini-3.5-flash-lite"
ACTOR_MODEL = (os.getenv("ACTOR_MODEL") or "").strip() or DEFAULT_MODEL
CRITIC_MODEL = (os.getenv("CRITIC_MODEL") or "").strip() or DEFAULT_MODEL
