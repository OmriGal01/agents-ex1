import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
PROMPTS_PATH = BASE_DIR / "prompts"
INFO_DOCS_PATH = BASE_DIR / "info-docs"

GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY") or "").strip()
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
DEFAULT_MODEL = "gemini-3.5-flash-lite"
ACTOR_MODEL = os.getenv("ACTOR_MODEL", DEFAULT_MODEL)
CRITIC_MODEL = os.getenv("CRITIC_MODEL", DEFAULT_MODEL)





