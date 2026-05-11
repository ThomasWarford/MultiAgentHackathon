"""Prompt template loading.

Templates are plain markdown with `{placeholder}` slots filled via str.format.
Keep them as files (not inline strings) so they're easy to iterate on without
touching Python code.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

_TEMPLATES_DIR = Path(__file__).parent


@lru_cache(maxsize=64)
def load_template(name: str) -> str:
    path = _TEMPLATES_DIR / f"{name}.md"
    if not path.is_file():
        raise FileNotFoundError(f"No prompt template named {name!r} at {path}.")
    return path.read_text(encoding="utf-8")


def render(name: str, **kwargs: object) -> str:
    return load_template(name).format(**kwargs)
