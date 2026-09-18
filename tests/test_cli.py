from pathlib import Path
from io import StringIO

import pytest

from llm_project_generator.cli import main
from llm_project_generator.providers import ProviderSpec


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


class InteractiveInput(StringIO):
    def isatty(self) -> bool:
        return True


class NonInteractiveInput(StringIO):
    def isatty(self) -> bool:
        return False


def test_explicit_provider_never_prompts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("builtins.input", lambda _prompt: pytest.fail("prompted"))

    assert main(["init", str(tmp_path / "explicit"), "--provider", "groq"]) == 0


def test_interactive_selection_displays_menu_and_generates(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("sys.stdin", InteractiveInput("1\n"))
    destination = tmp_path / "interactive"

    assert main(["init", str(destination)]) == 0

    output = capsys.readouterr().out
    assert "Select a provider:" in output
    assert "1. Groq" in output
    assert destination.exists()


def test_interactive_menu_uses_provider_display_name(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    import llm_project_generator.cli as cli

    custom = ProviderSpec("custom", "providers/groq", "Human Label")
    monkeypatch.setattr(cli, "PROVIDERS", (custom,))
    monkeypatch.setattr("sys.stdin", InteractiveInput("1\n"))

    assert cli._select_provider() == custom
    assert "1. Human Label" in capsys.readouterr().out


@pytest.mark.parametrize("selection", ["", "abc", "0", "-1", "2"])
def test_invalid_interactive_selection_prompts_again(
    selection: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("sys.stdin", InteractiveInput(f"{selection}\n1\n"))

    assert main(["init", str(tmp_path / "retry")]) == 0
    assert capsys.readouterr().err.count("Invalid provider number") == 1


def test_noninteractive_omission_fails_without_prompt_or_generation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    destination = tmp_path / "noninteractive"
    monkeypatch.setattr("sys.stdin", NonInteractiveInput())
    monkeypatch.setattr("builtins.input", lambda: pytest.fail("prompted"))

    assert main(["init", str(destination)]) == 2
    assert "--provider is required for non-interactive use" in capsys.readouterr().err
    assert not destination.exists()


@pytest.mark.parametrize("interruption", [EOFError, KeyboardInterrupt])
def test_interrupted_interactive_selection_exits_cleanly(
    interruption: type[BaseException],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("sys.stdin", InteractiveInput())

    def interrupt(_prompt: str) -> str:
        raise interruption

    monkeypatch.setattr("builtins.input", interrupt)
    destination = tmp_path / "cancelled"

    assert main(["init", str(destination)]) == 2
    assert "provider selection cancelled" in capsys.readouterr().err
    assert not destination.exists()


def test_help_describes_optional_interactive_provider(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["init", "--help"])

    assert exc_info.value.code == 0
    output = capsys.readouterr().out
    assert "--provider" in output
    assert "interactive selection" in output
