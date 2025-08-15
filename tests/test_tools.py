"""Tests for tool stubs."""

from agent_core.tools import fs


def test_read_file_stub() -> None:
    """read_file returns an empty string for now."""
    assert fs.read_file("foo") == ""
