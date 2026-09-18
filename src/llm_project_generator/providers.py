from dataclasses import dataclass

from llm_project_generator.errors import UnsupportedProviderError


@dataclass(frozen=True, slots=True)
class ProviderSpec:
    name: str
    template_name: str
    display_name: str


GROQ = ProviderSpec(
    name="groq",
    template_name="providers/groq",
    display_name="Groq",
)
GOOGLE = ProviderSpec(
    name="google",
    template_name="providers/google",
    display_name="Google Gemini",
)
OPENAI = ProviderSpec(
    name="openai",
    template_name="providers/openai",
    display_name="OpenAI",
)
PROVIDERS: tuple[ProviderSpec, ...] = (GROQ, GOOGLE, OPENAI)


def resolve_provider(name: str) -> ProviderSpec:
    for provider in PROVIDERS:
        if provider.name == name:
            return provider
    raise UnsupportedProviderError(f"Unsupported provider: {name}")
