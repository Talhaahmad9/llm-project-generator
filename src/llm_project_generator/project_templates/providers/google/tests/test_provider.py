from unittest.mock import Mock, patch

from app.config import Settings
from app.provider import create_agent


def test_create_agent_constructs_google_model_without_network() -> None:
    settings = Settings(google_api_key="test-key")
    with (
        patch("app.provider.GoogleProvider") as provider,
        patch("app.provider.GoogleModel") as model,
        patch("app.provider.Agent") as agent,
    ):
        model.return_value = Mock()
        create_agent(settings)
        provider.assert_called_once_with(api_key="test-key")
        model.assert_called_once_with(
            "gemini-3.5-flash-lite",
            provider=provider.return_value,
        )
        agent.assert_called_once_with(model.return_value, output_type=str)
