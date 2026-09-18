import pytest
import asyncio

from pydantic_ai import Agent, models
from pydantic_ai.models.test import TestModel

from app.exceptions import LLMError
from app.main import is_exit_command, main, run_chat
from app.config import Settings

models.ALLOW_MODEL_REQUESTS = False

@pytest.mark.parametrize(
    "command",
    [
        "exit",
        "quit",
        "EXIT",
        "Quit",
        "  exit  ",
    ],
)
def test_recognizes_exit_commands(
    command: str,
) -> None:
    assert is_exit_command(command) is True


@pytest.mark.parametrize(
    "command",
    [
        "",
        "hello",
        "exiting",
        "please quit now",
    ],
)
def test_rejects_non_exit_commands(
    command: str,
) -> None:
    assert is_exit_command(command) is False
    
def test_run_chat_prints_assistant_response(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    inputs = iter(["Hello", "exit"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt: next(inputs),
    )

    agent = Agent(
        TestModel(custom_output_text="Test response"),
        output_type=str,
    )

    asyncio.run(run_chat(agent))

    output = capsys.readouterr().out

    assert "Assistant: Test response" in output

def test_run_chat_handles_blank_input(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    inputs = iter(["   ", "exit"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt: next(inputs),
    )

    agent = Agent(
        TestModel(custom_output_text="Test response"),
        output_type=str,
    )

    asyncio.run(run_chat(agent))

    output = capsys.readouterr().out

    assert "Please enter a message." in output
    assert "Assistant:" not in output

def test_run_chat_reports_llm_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    inputs = iter(["Hello", "exit"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt: next(inputs),
    )

    async def failing_assistant(
        *_args: object,
    ) -> None:
        raise LLMError(
            "The language model request failed"
        )

    monkeypatch.setattr(
        "app.main.create_assistant_message",
        failing_assistant,
    )

    agent = Agent(
        TestModel(custom_output_text="Unused"),
        output_type=str,
    )

    asyncio.run(run_chat(agent))

    output = capsys.readouterr().out

    assert (
        "Error: The language model request failed"
        in output
    )

def test_main_creates_agent_and_runs_chat(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_settings = object()
    fake_agent = object()
    received: dict[str, object] = {}

    monkeypatch.setattr(
        "app.main.Settings",
        lambda: fake_settings,
    )

    def fake_create_agent(
        settings: object,
    ) -> object:
        received["settings"] = settings
        return fake_agent

    async def fake_run_chat(
        agent: object,
    ) -> None:
        received["agent"] = agent

    monkeypatch.setattr(
        "app.main.create_agent",
        fake_create_agent,
    )
    monkeypatch.setattr(
        "app.main.run_chat",
        fake_run_chat,
    )

    main()

    assert received["settings"] is fake_settings
    assert received["agent"] is fake_agent

@pytest.mark.parametrize(
    "interruption",
    [KeyboardInterrupt, EOFError],
)
def test_main_handles_terminal_interruption(
    interruption: type[BaseException],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fake_agent = object()

    monkeypatch.setattr(
        "app.main.Settings",
        lambda: object(),
    )
    monkeypatch.setattr(
        "app.main.create_agent",
        lambda _settings: fake_agent,
    )

    async def interrupted_run_chat(
        _agent: object,
    ) -> None:
        raise interruption

    monkeypatch.setattr(
        "app.main.run_chat",
        interrupted_run_chat,
    )

    try:
        main()
    except interruption:
        pytest.fail(
        f"main() did not handle "
        f"{interruption.__name__}"
    )

    output = capsys.readouterr().out

    assert "Goodbye!" in output
    
def test_main_reports_invalid_configuration(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        "app.main.Settings",
        lambda: Settings.model_validate({}),
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    output = capsys.readouterr().out

    assert exc_info.value.code == 2
    assert (
        "Configuration error: check your environment settings."
        in output
    )
