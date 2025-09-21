"""Tests for tool stubs."""

import pytest

from agent_core.tools import fs, shell


def test_read_file_returns_contents(tmp_path) -> None:
    """read_file should read the contents of a text file."""

    file_path = tmp_path / "sample.txt"
    file_path.write_text("example")

    assert fs.read_file(file_path) == "example"


def test_read_file_missing(tmp_path) -> None:
    """read_file raises FileToolError when path does not exist."""

    with pytest.raises(fs.FileToolError):
        fs.read_file(tmp_path / "missing.txt")


def test_shell_run_echo() -> None:
    """shell.run should execute commands and return output."""
    assert shell.run(["echo", "hello world"]) == "hello world\n"


def test_shell_run_failure() -> None:
    """shell.run should raise an error for non-zero exit codes."""
    with pytest.raises(shell.ShellCommandError) as exc:
        shell.run(["bash", "-lc", "exit 2"])

    assert exc.value.returncode == 2
