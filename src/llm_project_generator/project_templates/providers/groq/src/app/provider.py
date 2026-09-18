from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider

from app.config import Settings


def create_agent(settings: Settings) -> Agent[None, str]:
    provider = GroqProvider(api_key=settings.groq_api_key.get_secret_value())
    model = GroqModel(settings.llm_model.removeprefix("groq:"), provider=provider)
    return Agent(model, output_type=str)
