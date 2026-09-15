import asyncio
import pytest

from pydantic_ai import Agent, models, ModelMessage
from pydantic_ai.models.test import TestModel

from app.chat import create_assistant_message
from app.schemas import ChatMessage, MessageRole


models.ALLOW_MODEL_REQUESTS = False

def test_creates_assistant_message() -> None:
    agent = Agent(
        TestModel(custom_output_text="Hello from the assistant"),
        output_type=str,
    )
    user_message = ChatMessage(
        role="user",
        content="Hello",
    )

    assistant_message = asyncio.run(
        create_assistant_message(agent, user_message),
    )

    assert assistant_message.role == "assistant"
    assert assistant_message.content == "Hello from the assistant"
    
@pytest.mark.parametrize(
    "role",
    ["system", "assistant"],
)
def test_rejects_non_user_message(
    role: MessageRole,
) -> None:
    agent = Agent(
        TestModel(custom_output_text="Should not be returned"),
        output_type=str,
    )
    message = ChatMessage(
        role=role,
        content="Not a user message",
    )

    with pytest.raises(
        ValueError,
        match="Only user messages can be submitted",
    ):
        asyncio.run(
            create_assistant_message(agent, message),
        )

def test_updates_model_conversation_history() -> None:
    agent = Agent(
        TestModel(custom_output_text="Assistant response"),
        output_type=str,
    )
    history: list[ModelMessage] = []
    user_message = ChatMessage(
        role="user",
        content="User message",
    )

    asyncio.run(
        create_assistant_message(
            agent,
            user_message,
            history,
        )
    )

    assert len(history) == 2
