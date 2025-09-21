"""Sandboxed shell command tool."""

from __future__ import annotations

import subprocess
from typing import Sequence


class ShellCommandError(RuntimeError):
    """Raised when the shell command fails."""

    def __init__(self, command: Sequence[str], returncode: int, output: str) -> None:
        pretty_output = output.strip() if output else ""
        super().__init__(
            f"Command {list(command)} failed with exit code {returncode}:\n{pretty_output}"
        )
        self.command = list(command)
        self.returncode = returncode
        self.output = output


def run(command: Sequence[str]) -> str:
    """Execute a shell command and return its combined output."""

    if not command:
        raise ValueError("Shell command must not be empty")

    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:  # Command not found on the system
        raise ShellCommandError(command, 127, str(exc)) from exc

    combined_output = "".join(
        part for part in (result.stdout, result.stderr) if part
    )

    if result.returncode != 0:
        raise ShellCommandError(command, result.returncode, combined_output)

    return combined_output
