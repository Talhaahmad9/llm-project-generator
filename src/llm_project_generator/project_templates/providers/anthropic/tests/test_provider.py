from unittest.mock import Mock, patch

from app.config import Settings
from app.provider import create_agent


def test_create_agent_constructs_anthropic_model_without_network() -> None:
    settings = Settings(anthropic_api_key="test-key")
    with (
        patch("app.provider.AnthropicProvider") as provider,
        patch("app.provider.AnthropicModel") as model,
        patch("app.provider.Agent") as agent,
    ):
        model.return_value = Mock()
        create_agent(settings)
        provider.assert_called_once_with(api_key="test-key")
        model.assert_called_once_with(
            "claude-sonnet-5",
            provider=provider.return_value,
        )
        agent.assert_called_once_with(model.return_value, output_type=str)
