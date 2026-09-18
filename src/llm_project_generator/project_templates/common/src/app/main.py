import asyncio

from pydantic import ValidationError
from pydantic_ai import Agent, ModelMessage

from app.chat import create_assistant_message
from app.schemas import ChatMessage
from app.exceptions import LLMError
from app.provider import create_agent
from app.config import Settings

EXIT_COMMANDS = frozenset({"exit", "quit"})


def is_exit_command(command: str) -> bool:
    return command.strip().casefold() in EXIT_COMMANDS

async def run_chat(
    agent: Agent[None, str],
) -> None:
    message_history: list[ModelMessage] = []

    while True:
        user_input = input("You: ")

        if is_exit_command(user_input):
            return
        
        if not user_input.strip():
            print("Please enter a message.")
            continue

        user_message = ChatMessage(
            role="user",
            content=user_input,
        )

        try:
            assistant_message = await create_assistant_message(
                agent,
                user_message,
                message_history
            )
        except LLMError as exc:
            print(f"Error: {exc}")
            continue

        print(
            f"Assistant: {assistant_message.content}"
        )

def main() -> None:
    try:
        settings = Settings()
    except ValidationError:
        print(
            "Configuration error: check your environment settings."
        )
        raise SystemExit(2) from None

    agent = create_agent(settings)

    try:
        asyncio.run(run_chat(agent))
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
        
