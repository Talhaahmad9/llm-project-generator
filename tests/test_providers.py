import pytest

from llm_project_generator.errors import UnsupportedProviderError
from llm_project_generator.providers import resolve_provider


def test_resolves_groq_exactly() -> None:
    provider = resolve_provider("groq")
    assert provider.name == "groq"
    assert provider.template_name == "groq_chatbot"


@pytest.mark.parametrize("name", ["Groq", "GROQ", "openai", ""])
def test_rejects_unknown_or_incorrectly_cased_provider(name: str) -> None:
    with pytest.raises(UnsupportedProviderError):
        resolve_provider(name)
