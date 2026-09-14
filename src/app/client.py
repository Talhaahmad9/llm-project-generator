from pydantic_ai import Agent, ModelMessage 
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
from pydantic_ai.exceptions import AgentRunError

from app.config import Settings
from app.exceptions import LLMError

def create_agent(settings: Settings) -> Agent[None, str]:
    api_key = settings.groq_api_key.get_secret_value()
    model_name = settings.llm_model.removeprefix("groq:")
    
    provider = GroqProvider(api_key=api_key)
    model = GroqModel(model_name, provider=provider)
    
    return Agent(model, output_type=str)

async def generate_reply(
    agent: Agent[None, str],
    prompt: str,
    message_history: list[ModelMessage] | None = None,
) -> str:
    try:
        result = await agent.run(
            prompt,
            message_history=message_history
            )
    except AgentRunError as exc:
        raise LLMError(
            "The language model request failed"
        ) from exc
    
    response = result.output
    
    if not response.strip():
        raise LLMError(
            "The language model returned an empty response"
        )
        
    if message_history is not None:
        message_history.extend(result.new_messages())
            
    return response
    
    