from typing import Never

import asyncio
import pytest

from pydantic_ai import (
    Agent,
    ModelMessage,
    ModelResponse,
    TextPart,
    models,
)
from pydantic_ai.models.test import TestModel
from pydantic_ai.models.function import AgentInfo, FunctionModel
from pydantic_ai.exceptions import AgentRunError
from app.client import generate_reply

from app.exceptions import LLMError


models.ALLOW_MODEL_REQUESTS = False

def test_generate_reply_returns_model_output() -> None:
    agent = Agent(
        TestModel(custom_output_text="Test response"),
        output_type=str,
    )

    response = asyncio.run(
        generate_reply(agent, "Hello"),
    )

    assert response == "Test response"
    
def fail_model(
    _messages: list[ModelMessage],
    _info: AgentInfo,
) -> Never:
    raise AgentRunError("Sensitive provider details")

def test_generate_reply_translates_agent_error() -> None:
    agent = Agent(
        FunctionModel(fail_model),
        output_type=str,
    )

    with pytest.raises(LLMError) as exc_info:
        asyncio.run(
            generate_reply(agent, "Hello"),
        )

    assert str(exc_info.value) == "The language model request failed"
    assert isinstance(exc_info.value.__cause__, AgentRunError)

def test_generate_reply_preserves_conversation_history() -> None:
    received_message_counts: list[int] = []

    def record_messages(
        messages: list[ModelMessage],
        _info: AgentInfo,
    ) -> ModelResponse:
        received_message_counts.append(len(messages))

        return ModelResponse(
            parts=[TextPart("Test response")]
        )

    agent = Agent(
        FunctionModel(record_messages),
        output_type=str,
    )
    history: list[ModelMessage] = []

    async def run_two_turns() -> None:
        await generate_reply(agent, "First message", history)
        await generate_reply(agent, "Second message", history)

    asyncio.run(run_two_turns())

    assert received_message_counts == [1, 3]
    assert len(history) == 4
    
@pytest.mark.parametrize(
    "output",
    ["   ", "\t\n"],
)
def test_rejects_whitespace_only_model_output(
    output: str,
) -> None:
    agent = Agent(
        TestModel(custom_output_text=output),
        output_type=str,
    )
    history: list[ModelMessage] = []

    with pytest.raises(
        LLMError,
        match="empty response",
    ):
        asyncio.run(
            generate_reply(
                agent,
                "Hello",
                history,
            )
        )

    assert history == []