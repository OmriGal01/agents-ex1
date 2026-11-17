import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
PROMPTS_PATH = BASE_DIR / "prompts"
INFO_DOCS_PATH = BASE_DIR / "info-docs"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

