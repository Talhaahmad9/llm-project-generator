# Anthropic Claude Terminal Chatbot

This terminal chatbot uses the direct Anthropic Claude API through Pydantic AI. It does not support AWS Bedrock, Vertex AI, Microsoft Foundry, gateways, proxy endpoints, tools, thinking configuration, or streaming.

## Requirements and setup

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- Anthropic API access, which may require credits or billing

Create a key in the [Anthropic Console](https://console.anthropic.com/settings/keys), then run:

```bash
uv sync
cp .env.example .env
```

`ANTHROPIC_API_KEY` is required. `LLM_MODEL` is optional and defaults to `anthropic:claude-sonnet-5`. Model availability and pricing can change, so consult the current Anthropic documentation before selecting a model.

## Run

```bash
uv run llm-chat
```

Enter `exit` or `quit` to end the session. Blank input is rejected, and Ctrl+C or EOF ends the session with `Goodbye!`.

## Test

```bash
uv run pytest
```

Tests use deterministic fake models and mocked provider construction. Normal tests make no Anthropic API requests.

## Architecture and security

Shared modules own chat validation, reply execution, terminal behavior, schemas, and exceptions. `config.py` owns Anthropic settings and `provider.py` owns `AnthropicProvider`, `AnthropicModel`, and agent construction. Common `client.py` remains provider-independent.

Keep `.env` private and never commit or print `ANTHROPIC_API_KEY`; `SecretStr` masks its normal representation. Model output is untrusted probabilistic data and is not an authorization or security boundary.

## Official documentation

- [Pydantic AI Anthropic models](https://pydantic.dev/docs/ai/models/anthropic/)
- [Claude models overview](https://platform.claude.com/docs/en/models/overview)
- [Claude model IDs and versions](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)
- [Claude model deprecations](https://docs.anthropic.com/en/docs/about-claude/model-deprecations)
- [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing)

## License

This project is licensed under the MIT License. Copyright (c) 2026 Talha Ahmad.
