from pydantic_ai import Agent, ModelMessage

from app.client import generate_reply
from app.schemas import ChatMessage

async def create_assistant_message(
    agent: Agent[None, str],
    user_message: ChatMessage,
    message_history: list[ModelMessage] | None = None,
) -> ChatMessage:
    if user_message.role != "user":
        raise ValueError(
            "Only user messages can be submitted"
        )

    response_content = await generate_reply(
        agent,
        user_message.content,
        message_history,
    )

    return ChatMessage(
        role="assistant",
        content=response_content,
    )