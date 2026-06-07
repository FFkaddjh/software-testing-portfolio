"""Tests for ANSI escape sequence stripping in pytest-reportlog."""

import json
import re
import pytest


@pytest.mark.parametrize(
    "input_data, expected",
    [
        # Simple string with ANSI escape sequences
        ("\x1b[31mhello\x1b[0m", "hello"),
        # String without ANSI escape sequences
        ("hello world", "hello world"),
        # Dict with ANSI in values
        ({"msg": "\x1b[31mError\x1b[0m", "level": "error"}, {"msg": "Error", "level": "error"}),
        # Nested dict with ANSI
        ({"outer": {"inner": "\x1b[1mbold\x1b[0m"}}, {"outer": {"inner": "bold"}}),
        # List with ANSI strings
        (["\x1b[32mok\x1b[0m", "normal"], ["ok", "normal"]),
        # Multiple ANSI sequences in one string
        ("\x1b[31mRed\x1b[0m and \x1b[32mGreen\x1b[0m", "Red and Green"),
        # Mixed types (int, None should be untouched)
        ({"value": 42, "name": "\x1b[36mtest\x1b[0m"}, {"value": 42, "name": "test"}),
    ],
)
def test_strip_ansi_from_data(input_data, expected):
    """Verify that ANSI escape sequences are properly stripped."""
    from pytest_reportlog.plugin import _strip_ansi_from_data

    result = _strip_ansi_from_data(input_data)
    assert result == expected, f"Expected {expected}, got {result}"


def test_ansi_stripping_does_not_affect_normal_data():
    """Verify that normal data without ANSI sequences passes through unchanged."""
    from pytest_reportlog.plugin import _strip_ansi_from_data

    data = {
        "pytest_version": "8.0.0",
        "$report_type": "SessionStart",
        "items": ["test_a", "test_b"],
        "counts": [1, 2, 3],
        "metadata": {"key": "value"},
    }
    assert _strip_ansi_from_data(data) == data


def test_ansi_stripping_preserves_data_structure():
    """Verify that data structure is preserved after stripping."""
    from pytest_reportlog.plugin import _strip_ansi_from_data

    data = {
        "sections": [
            ("Captured log call", "\x1b[33mWARNING\x1b[0m something happened"),
            ("Captured stdout", "normal output"),
        ]
    }
    expected = {
        "sections": [
            ("Captured log call", "WARNING something happened"),
            ("Captured stdout", "normal output"),
        ]
    }
    result = _strip_ansi_from_data(data)
    assert result == expected


def test_complex_ansi_sequences():
    """Test that various ANSI escape sequence patterns are stripped."""
    from pytest_reportlog.plugin import _strip_ansi_from_data

    test_cases = [
        ("\x1b[1m", ""),             # Bold
        ("\x1b[3m", ""),             # Italic
        ("\x1b[4m", ""),             # Underline
        ("\x1b[38;5;196m", ""),      # 256 color
        ("\x1b[48;5;27m", ""),       # 256 background
        ("\x1b[91m", ""),            # Bright red
        ("\x1b[92;103m", ""),        # Multiple color codes
        ("\x1b[?25l", ""),           # Cursor hide (private sequence)
        ("\x1b[2J", ""),             # Clear screen
        ("text\x1b[31;1m", "text"),  # Text before escape
    ]
    for inp, expected in test_cases:
        assert _strip_ansi_from_data(inp) == expected, f"Failed for input: {repr(inp)}"


def test_integration_with_report_log(testdir, tmp_path):
    """Integration test: ANSI-stripped output should be valid JSON."""
    p = testdir.makepyfile("""
        def test_ok():
            pass

        def test_fail():
            assert [1] == [2]  # This should produce colored diff output
    """)

    log_file = tmp_path / "log.json"
    result = testdir.runpytest("--report-log", str(log_file))

    # Read log file and verify all lines parse as valid JSON
    with open(str(log_file), "r", encoding="UTF-8") as f:
        for line in f:
            data = json.loads(line)
            # Verify no ANSI escape sequences remain in any string values
            json_str = json.dumps(data)
            assert "\x1b[" not in json_str, f"Found ANSI escape in: {json_str[:200]}"


def test_cleanup_unserializable_with_ansi(testdir):
    """Test that cleanup_unserializable handles data that also needs ANSI stripping."""
    from pytest_reportlog.plugin import _strip_ansi_from_data, cleanup_unserializable

    class CustomObj:
        def __str__(self):
            return "\x1b[31mCustom\x1b[0m Error"

    data = {"error": CustomObj(), "message": "\x1b[33mWarning\x1b[0m"}
    cleaned = cleanup_unserializable(data)
    stripped = _strip_ansi_from_data(cleaned)
    assert stripped == {"error": "Custom Error", "message": "Warning"}
