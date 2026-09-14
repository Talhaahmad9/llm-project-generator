from pathlib import Path

import pytest

from llm_project_generator.cli import main


def test_cli_success(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    destination = tmp_path / "chatbot"
    assert main(["init", str(destination), "--provider", "groq"]) == 0
    output = capsys.readouterr().out
    assert "chatbot" in output
    assert "groq" in output


def test_cli_reports_expected_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    destination = tmp_path / "chatbot"
    assert main(["init", str(destination), "--provider", "GROQ"]) == 1
    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert captured.out == ""
    assert not destination.exists()
