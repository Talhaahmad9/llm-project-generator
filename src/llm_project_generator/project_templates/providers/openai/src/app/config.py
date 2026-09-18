from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    openai_api_key: SecretStr
    llm_model: str = "openai:gpt-5.4-mini"

    @field_validator("openai_api_key")
    @classmethod
    def openai_api_key_must_not_be_blank(cls, value: SecretStr) -> SecretStr:
        if not value.get_secret_value().strip():
            raise ValueError("OPENAI API Key must not be blank")
        return value

    @field_validator("llm_model")
    @classmethod
    def llm_model_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("LLM model must not be blank")
        return value
