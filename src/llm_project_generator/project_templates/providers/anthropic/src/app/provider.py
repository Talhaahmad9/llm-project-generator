from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider

from app.config import Settings


def create_agent(settings: Settings) -> Agent[None, str]:
    provider = AnthropicProvider(api_key=settings.anthropic_api_key.get_secret_value())
    model = AnthropicModel(
        settings.llm_model.removeprefix("anthropic:"),
        provider=provider,
    )
    return Agent(model, output_type=str)
