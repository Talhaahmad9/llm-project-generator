import pytest
from pydantic import ValidationError

from app.schemas import ChatMessage, MessageRole


@pytest.mark.parametrize("role", ["system", "user", "assistant"])
def test_accepts_each_valid_role(role: MessageRole) -> None:
    message = ChatMessage(role=role, content="Hello")

    assert message.role == role
    assert message.content == "Hello"

@pytest.mark.parametrize("content", ["", "   ", "\t\n"])
def test_rejects_blank_content(content: str) -> None:
    invalid_data = {
        "role": "user",
        "content": content,
    }
    
    with pytest.raises(ValidationError):
        ChatMessage.model_validate(invalid_data)

def test_rejects_unknown_role() -> None:
    invalid_data = {
        "role": "admin",
        "content": "Hello",
    }

    with pytest.raises(ValidationError):
        ChatMessage.model_validate(invalid_data)

def test_preserves_meaningful_whitespace() -> None:
    original_content = "  Hello\n"

    message = ChatMessage(role="user", content=original_content)

    assert message.content == original_content
    
@pytest.mark.parametrize(
    "invalid_data",
    [
        {"content": "Hello"},
        {"role": "user"},
    ],
    ids=["missing-role", "missing-content"],
)
def test_rejects_missing_required_field(
    invalid_data: dict[str, str],
) -> None:
    with pytest.raises(ValidationError):
        ChatMessage.model_validate(invalid_data)

@pytest.mark.parametrize(
    "invalid_data",
    [
        {"role": 123, "content": "Hello"},
        {"role": None, "content": "Hello"},
        {"role": "user", "content": 123},
        {"role": "user", "content": None},
    ],
    ids=[
        "role-is-integer",
        "role-is-none",
        "content-is-integer",
        "content-is-none",
    ],
)
def test_rejects_incorrect_field_types(
    invalid_data: dict[str, object],
) -> None:
    with pytest.raises(ValidationError):
        ChatMessage.model_validate(invalid_data)

def test_rejects_unknown_fields() -> None:
    invalid_data = {
        "role": "user",
        "content": "Hello",
        "unexpected": "value",
    }

    with pytest.raises(ValidationError):
        ChatMessage.model_validate(invalid_data)