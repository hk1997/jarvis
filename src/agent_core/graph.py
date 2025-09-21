"""State machine orchestrator for agents."""

from __future__ import annotations

import re
import shlex
from typing import Callable, Iterable, Sequence

from .tools import shell


SHELL_TRIGGER_PATTERN = re.compile(r"(run|execute)\s+shell\s+command", re.IGNORECASE)


class AgentGraph:
    """Simple agent that can execute shell commands when instructed."""

    def __init__(
        self, *, shell_runner: Callable[[Sequence[str]], str] = shell.run
    ) -> None:
        self._shell_runner = shell_runner

    def handle_instruction(self, instruction: str) -> str:
        """Process an instruction and invoke the appropriate tool."""

        command = self._extract_shell_command(instruction)
        if command is None:
            raise ValueError("No shell command instruction detected")

        return self._shell_runner(command)

    def _extract_shell_command(self, instruction: str) -> Sequence[str] | None:
        """Return command tokens if the instruction targets the shell tool."""

        if not instruction or not SHELL_TRIGGER_PATTERN.search(instruction):
            return None

        command_text = self._extract_command_text(instruction)
        if command_text is None:
            return None

        try:
            tokens = shlex.split(command_text)
        except ValueError as exc:  # unmatched quotes or similar parsing issues
            raise ValueError(f"Invalid command syntax: {exc}") from exc

        return tokens if tokens else None

    @staticmethod
    def _extract_command_text(instruction: str) -> str | None:
        """Extract raw command text from an instruction."""

        segments: Iterable[str] = (
            AgentGraph._command_after_colon(instruction),
            AgentGraph._command_in_backticks(instruction),
            AgentGraph._command_after_keyword(instruction),
        )

        for segment in segments:
            if segment:
                return segment

        return None

    @staticmethod
    def _command_after_colon(instruction: str) -> str | None:
        """Return text following the first colon if it looks like a command."""

        prefix, _, suffix = instruction.partition(":")
        if suffix and SHELL_TRIGGER_PATTERN.search(prefix):
            return suffix.strip()
        return None

    @staticmethod
    def _command_in_backticks(instruction: str) -> str | None:
        """Return the first substring enclosed in backticks."""

        match = re.search(r"`([^`]+)`", instruction)
        if match:
            return match.group(1).strip()
        return None

    @staticmethod
    def _command_after_keyword(instruction: str) -> str | None:
        """Return text immediately following the word 'command'."""

        match = re.search(r"command(?:\s+to)?\s+(.+)$", instruction, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None
