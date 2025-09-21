"""Local file operations tool."""

from __future__ import annotations

from pathlib import Path
from typing import Union


class FileToolError(RuntimeError):
    """Raised when a file operation fails."""

    def __init__(self, path: Union[str, Path], message: str) -> None:
        resolved = str(Path(path).expanduser())
        super().__init__(f"{resolved}: {message}")
        self.path = resolved
        self.message = message


def read_file(path: Union[str, Path], *, encoding: str = "utf-8") -> str:
    """Return the text content of a file using the provided encoding."""

    if not path:
        raise ValueError("File path must not be empty")

    file_path = Path(path).expanduser()

    if not file_path.exists():
        raise FileToolError(file_path, "No such file or directory")

    if not file_path.is_file():
        raise FileToolError(file_path, "Path is not a file")

    try:
        return file_path.read_text(encoding=encoding)
    except UnicodeDecodeError as exc:
        raise FileToolError(file_path, f"Unable to decode file with encoding '{encoding}'") from exc
