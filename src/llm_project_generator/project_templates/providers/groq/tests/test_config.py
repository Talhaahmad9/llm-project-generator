import pytest
from pydantic import ValidationError
from pathlib import Path

from app.config import Settings

def test_loads_api_key_and_default_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.delenv("LLM_MODEL", raising=False)

    settings = Settings(_env_file=None)

    assert settings.groq_api_key.get_secret_value() == "test-key"
    assert settings.llm_model == "groq:openai/gpt-oss-120b"

def test_rejects_missing_api_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    with pytest.raises(ValidationError) as exc_info:
        Settings(_env_file=None)

    error = exc_info.value.errors()[0]

    assert error["loc"] == ("groq_api_key",)
    assert error["type"] == "missing"

def test_environment_overrides_default_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.setenv(
        "LLM_MODEL",
        "groq:llama-3.1-8b-instant",
    )

    settings = Settings(_env_file=None)

    assert settings.llm_model == "groq:llama-3.1-8b-instant"

def test_masks_api_key_in_display(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_key = "test-secret-key"
    monkeypatch.setenv("GROQ_API_KEY", fake_key)

    settings = Settings(_env_file=None)

    assert fake_key not in str(settings.groq_api_key)
    assert fake_key not in repr(settings)

def test_loads_values_from_env_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("LLM_MODEL", raising=False)

    env_file = tmp_path / ".env"
    env_file.write_text(
        "GROQ_API_KEY=file-test-key\n"
        "LLM_MODEL=groq:test-model\n",
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.groq_api_key.get_secret_value() == "file-test-key"
    assert settings.llm_model == "groq:test-model"

@pytest.mark.parametrize(
    "api_key",
    ["", "   ", "\t\n"],
)
def test_rejects_blank_api_key(
    monkeypatch: pytest.MonkeyPatch,
    api_key: str,
) -> None:
    monkeypatch.setenv("GROQ_API_KEY", api_key)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)

@pytest.mark.parametrize(
    "model",
    ["", "   ", "\t\n"],
)
def test_rejects_blank_model(
    monkeypatch: pytest.MonkeyPatch,
    model: str,
) -> None:
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.setenv("LLM_MODEL", model)

    with pytest.raises(ValidationError) as exc_info:
        Settings(_env_file=None)

    error = exc_info.value.errors()[0]

    assert error["loc"] == ("llm_model",)
    assert error["type"] == "value_error"