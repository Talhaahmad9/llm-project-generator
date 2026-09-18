from unittest.mock import Mock, patch

from app.config import Settings
from app.provider import create_agent


def test_create_agent_constructs_groq_model_without_network() -> None:
    settings = Settings(groq_api_key="test-key")
    with patch("app.provider.GroqProvider") as provider, patch("app.provider.GroqModel") as model, patch("app.provider.Agent") as agent:
        model.return_value = Mock()
        create_agent(settings)
        provider.assert_called_once_with(api_key="test-key")
        model.assert_called_once_with("openai/gpt-oss-120b", provider=provider.return_value)
        agent.assert_called_once_with(model.return_value, output_type=str)
