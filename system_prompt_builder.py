from pathlib import Path

from config import INFO_DOCS_PATH, PROMPTS_PATH

SUPPORTED_TEXT_EXTENSIONS = {".md", ".txt"}
DEFAULT_SYSTEM_PROMPT_FILE = PROMPTS_PATH / "system-prompt.md"


def read_document(file_path: Path) -> str:
    """Read text content from a markdown or text file."""
    suffix = file_path.suffix.lower()

    if suffix in SUPPORTED_TEXT_EXTENSIONS:
        return file_path.read_text(encoding="utf-8").strip()

    raise ValueError(f"Unsupported file extension: {file_path.suffix}")


def load_background_docs(info_docs_dir: Path = INFO_DOCS_PATH) -> str:
    """Load and concatenate all markdown/text background documents from info_docs_dir."""
    if not info_docs_dir.exists() or not info_docs_dir.is_dir():
        raise FileNotFoundError(f"Info docs directory not found: {info_docs_dir}")

    doc_sections: list[str] = []

    for file_path in sorted(info_docs_dir.iterdir()):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_TEXT_EXTENSIONS:
            content = read_document(file_path)
            if content:
                doc_sections.append(f"--- Document: {file_path.name} ---\n{content}")

    if not doc_sections:
        raise ValueError(f"No readable background documents found in: {info_docs_dir}")

    return "\n\n".join(doc_sections)


def build_system_prompt(
    prompt_file: Path = DEFAULT_SYSTEM_PROMPT_FILE,
    info_docs_dir: Path = INFO_DOCS_PATH,
) -> str:
    """Build the final system prompt by injecting the background documents."""
    if not prompt_file.exists():
        raise FileNotFoundError(f"System prompt file not found: {prompt_file}")

    template = prompt_file.read_text(encoding="utf-8")
    background_docs = load_background_docs(info_docs_dir)

    return template.replace("{background_docs}", background_docs)


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    print(build_system_prompt())
