from functools import lru_cache
from pathlib import Path

SUPPORTED_TEXT_EXTENSIONS = {".md", ".txt"}


def read_document(file_path: Path) -> str:
    """Read text content from a markdown or text file."""
    suffix = file_path.suffix.lower()

    if suffix in SUPPORTED_TEXT_EXTENSIONS:
        return file_path.read_text(encoding="utf-8").strip()

    raise ValueError(f"Unsupported file extension: {file_path.suffix}")


@lru_cache(maxsize=16)
def load_docs(docs_dir: Path) -> str:
    """Load and concatenate all supported text/markdown documents from a directory."""
    docs_dir = Path(docs_dir).resolve()
    if not docs_dir.exists() or not docs_dir.is_dir():
        raise FileNotFoundError(f"Documents directory not found: {docs_dir}")

    doc_sections: list[str] = []

    for file_path in sorted(docs_dir.iterdir()):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_TEXT_EXTENSIONS:
            content = read_document(file_path)
            if content:
                doc_sections.append(f"--- Document: {file_path.name} ---\n{content}")

    if not doc_sections:
        raise ValueError(f"No readable documents found in: {docs_dir}")

    return "\n\n".join(doc_sections)


def build_prompt(
    prompt_file: Path,
    docs_dir: Path | None = None,
    **placeholders: str,
) -> str:
    """Build a prompt from a template file, injecting docs_dir and any named placeholders."""
    prompt_file = Path(prompt_file)
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

    prompt = prompt_file.read_text(encoding="utf-8")

    if docs_dir is not None:
        placeholders.setdefault("background_docs", load_docs(Path(docs_dir)))

    for key, value in placeholders.items():
        prompt = prompt.replace(f"{{{key}}}", str(value))

    return prompt
