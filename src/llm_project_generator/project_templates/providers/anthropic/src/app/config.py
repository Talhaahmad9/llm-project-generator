from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    anthropic_api_key: SecretStr
    llm_model: str = "anthropic:claude-sonnet-5"

    @field_validator("anthropic_api_key")
    @classmethod
    def anthropic_api_key_must_not_be_blank(cls, value: SecretStr) -> SecretStr:
        if not value.get_secret_value().strip():
            raise ValueError("ANTHROPIC API Key must not be blank")
        return value

    @field_validator("llm_model")
    @classmethod
    def llm_model_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("LLM model must not be blank")
        return value
