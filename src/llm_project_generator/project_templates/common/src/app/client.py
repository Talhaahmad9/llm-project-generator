from pydantic_ai import Agent, ModelMessage 
from pydantic_ai.exceptions import AgentRunError

from app.exceptions import LLMError

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
    
    
