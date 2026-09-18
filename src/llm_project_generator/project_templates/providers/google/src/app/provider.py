from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from app.config import Settings


def create_agent(settings: Settings) -> Agent[None, str]:
    provider = GoogleProvider(api_key=settings.google_api_key.get_secret_value())
    model = GoogleModel(settings.llm_model.removeprefix("google:"), provider=provider)
    return Agent(model, output_type=str)
