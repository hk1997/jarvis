"""Tests for tool stubs."""

import pytest

from agent_core.tools import fs, shell


def test_read_file_stub() -> None:
    """read_file returns an empty string for now."""
    assert fs.read_file("foo") == ""


def test_shell_run_echo() -> None:
    """shell.run should execute commands and return output."""
    assert shell.run(["echo", "hello world"]) == "hello world\n"


def test_shell_run_failure() -> None:
    """shell.run should raise an error for non-zero exit codes."""
    with pytest.raises(shell.ShellCommandError) as exc:
        shell.run(["bash", "-lc", "exit 2"])

    assert exc.value.returncode == 2
