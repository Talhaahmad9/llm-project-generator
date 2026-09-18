import pytest

from llm_project_generator.errors import UnsupportedProviderError
from llm_project_generator.providers import PROVIDERS, resolve_provider


def test_resolves_groq_exactly() -> None:
    provider = resolve_provider("groq")
    assert provider.name == "groq"
    assert provider.template_name == "providers/groq"
    assert provider.display_name == "Groq"


def test_resolves_google_exactly() -> None:
    provider = resolve_provider("google")
    assert provider.name == "google"
    assert provider.display_name == "Google Gemini"
    assert provider.template_name == "providers/google"


def test_provider_order_is_deterministic() -> None:
    assert [provider.name for provider in PROVIDERS] == ["groq", "google", "openai", "anthropic"]


def test_resolves_openai_exactly() -> None:
    provider = resolve_provider("openai")
    assert provider.name == "openai"
    assert provider.display_name == "OpenAI"
    assert provider.template_name == "providers/openai"


def test_resolves_anthropic_exactly() -> None:
    provider = resolve_provider("anthropic")
    assert provider.name == "anthropic"
    assert provider.display_name == "Anthropic Claude"
    assert provider.template_name == "providers/anthropic"


@pytest.mark.parametrize(
    "name",
    ["Groq", "GROQ", "Google", "GOOGLE", "gemini", "OpenAI", "OPENAI", "openai-chat", "Anthropic", "ANTHROPIC", "claude", "sonnet", ""],
)
def test_rejects_unknown_or_incorrectly_cased_provider(name: str) -> None:
    with pytest.raises(UnsupportedProviderError):
        resolve_provider(name)
