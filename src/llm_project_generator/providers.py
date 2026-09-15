from dataclasses import dataclass

from llm_project_generator.errors import UnsupportedProviderError


@dataclass(frozen=True, slots=True)
class ProviderSpec:
    name: str
    template_name: str


GROQ = ProviderSpec(name="groq", template_name="groq_chatbot")
PROVIDERS: tuple[ProviderSpec, ...] = (GROQ,)


def resolve_provider(name: str) -> ProviderSpec:
    for provider in PROVIDERS:
        if provider.name == name:
            return provider
    raise UnsupportedProviderError(f"Unsupported provider: {name}")
