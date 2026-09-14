from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator


type MessageRole = Literal["system", "user", "assistant"]

class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    role: MessageRole
    content: str
    
    @field_validator("content")
    @classmethod
    def content_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Content must not be blank")
        
        return value