# Google Gemini Terminal Chatbot

This is a terminal chatbot using the Google Gemini Developer API through Google AI Studio and Pydantic AI. It does not provide Vertex AI support, web APIs, RAG, persistence, or multi-provider routing.

## Requirements and setup

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- A Google AI Studio API key

Create a key at [Google AI Studio](https://aistudio.google.com/apikey), then set it up:

```bash
uv sync
cp .env.example .env
```

`GOOGLE_API_KEY` is required. `LLM_MODEL` is optional and defaults to `google:gemini-3.5-flash-lite`. The `google:` prefix is removed before constructing the Pydantic AI Google model. This project uses the Gemini Developer API, not Vertex AI or Google Cloud credentials.

## Run

```bash
uv run llm-chat
```

Enter `exit` or `quit` to end the session. Blank input is rejected, and Ctrl+C or EOF ends the session with `Goodbye!`.

## Test

```bash
uv run pytest
```

Tests use deterministic fake models and mocked provider construction. Normal tests disable real model requests and do not contact Google.

## Architecture and security

The shared application modules own chat validation, reply execution, terminal behavior, schemas, and exceptions. `config.py` owns Google settings and `provider.py` owns `GoogleProvider`, `GoogleModel`, and agent construction. Common `client.py` remains provider-independent.

Keep `.env` private and never commit or print `GOOGLE_API_KEY`; `SecretStr` protects its representation. Model output is untrusted probabilistic data and is not an authorization or security boundary. Google free-tier availability and quotas may vary; review current free-tier data-handling terms before sending sensitive data.

## Official documentation

- [Pydantic AI Google models](https://pydantic.dev/docs/ai/models/google/)
- [Gemini API models](https://ai.google.dev/gemini-api/docs/models)
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Gemini API deprecations](https://ai.google.dev/gemini-api/docs/deprecations)

## License

This project is licensed under the MIT License. Copyright (c) 2026 Talha Ahmad.
