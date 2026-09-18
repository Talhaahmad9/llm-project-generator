# OpenAI Responses API Terminal Chatbot

This terminal chatbot uses Pydantic AI's modern OpenAI Responses API integration. It does not use Chat Completions, Azure OpenAI, OpenAI-compatible endpoints, Codex OAuth, tools, or streaming.

## Requirements and setup

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- An eligible billed OpenAI API account

Create an API key at [OpenAI API keys](https://platform.openai.com/api-keys), then run:

```bash
uv sync
cp .env.example .env
```

`OPENAI_API_KEY` is required. `LLM_MODEL` is optional and defaults to `openai:gpt-5.4-mini`. ChatGPT subscriptions are separate from ordinary OpenAI API billing.

## Run

```bash
uv run llm-chat
```

Enter `exit` or `quit` to end the session. Blank input is rejected, and Ctrl+C or EOF ends the session with `Goodbye!`.

## Test

```bash
uv run pytest
```

Tests use deterministic fake models and mocked provider construction. Normal tests make no OpenAI API requests.

## Architecture and security

Shared modules own chat validation, reply execution, terminal behavior, schemas, and exceptions. `config.py` owns OpenAI settings and `provider.py` owns `OpenAIProvider`, `OpenAIResponsesModel`, and agent construction. Common `client.py` remains provider-independent.

Keep `.env` private and never commit or print `OPENAI_API_KEY`; `SecretStr` masks its normal representation. Model output is untrusted probabilistic data and is not an authorization or security boundary.

## Official documentation

- [Pydantic AI OpenAI models](https://pydantic.dev/docs/ai/models/openai/)
- [GPT-5.4 mini](https://developers.openai.com/api/docs/models/gpt-5.4-mini)
- [OpenAI models](https://developers.openai.com/api/docs/models)
- [OpenAI API pricing](https://openai.com/api/pricing/)

## License

This project is licensed under the MIT License. Copyright (c) 2026 Talha Ahmad.
