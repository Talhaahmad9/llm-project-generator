from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider

from app.config import Settings


def create_agent(settings: Settings) -> Agent[None, str]:
    provider = OpenAIProvider(api_key=settings.openai_api_key.get_secret_value())
    model = OpenAIResponsesModel(
        settings.llm_model.removeprefix("openai:"),
        provider=provider,
    )
    return Agent(model, output_type=str)
