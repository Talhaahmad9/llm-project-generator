# Groq Terminal Chatbot

This is a terminal-based chatbot built with [Pydantic AI](https://ai.pydantic.dev/) and Groq.

## Scope

The application is a terminal chat loop using Groq only. It does not provide a web API, RAG, autonomous agentic workflows, tool calling, persistence, or multi-provider routing.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- A Groq API key

Set up the project from Git Bash:

```bash
uv sync
cp .env.example .env
```

Obtain a key from the [Groq Console](https://console.groq.com/keys), then put your own key in `.env` as `GROQ_API_KEY`. Never commit that file or share its contents.

### Configuration

| Variable | Required | Behavior |
| --- | --- | --- |
| `GROQ_API_KEY` | Yes | The Groq credential used to create the client. It must not be blank. |
| `LLM_MODEL` | No | Overrides the default model. The current default is `groq:openai/gpt-oss-120b`. |

The model setting is passed to the Groq integration after its `groq:` prefix is removed. Do not assume arbitrary provider prefixes are supported. Before changing the value, check Groq's current [supported models](https://console.groq.com/docs/models) and [model deprecations](https://console.groq.com/docs/deprecations).

## Run

```bash
uv run llm-chat
```

The program reads a prompt after `You: ` and prints the response after `Assistant: `. Conversation history is kept in memory for the current run only; it is not persisted after exit.

Enter `exit` or `quit` to end the session. Matching is case-insensitive and surrounding whitespace is ignored. Blank input prints `Please enter a message.` and waits for another prompt. Ctrl+C and EOF end the session with `Goodbye!`.

## Test

```bash
uv run pytest
```

The tests use Pydantic AI test and fake clients, including deterministic model responses and failure cases. The normal test suite does not intentionally make paid or live Groq requests.

## Architecture

The application dependency direction is:

```text
main.py -> chat.py -> client.py and provider.py -> Groq/Pydantic AI
```

- `main.py` owns the terminal loop, commands, input handling, and top-level configuration/interruption messages.
- `chat.py` validates that submitted messages are user messages and creates assistant messages.
- `client.py` owns provider-independent reply execution and translates known model-run failures into `LLMError`.
- `provider.py` constructs the Groq model and agent.
- `config.py` loads `.env` and environment variables with Pydantic Settings, validates required values, and uses `SecretStr` for the API key.
- `schemas.py` defines validated chat messages and their allowed roles.
- `exceptions.py` contains the application error hierarchy.

## Security

`.env` is ignored by Git and is never intended for commits. Do not print or log `SecretStr.get_secret_value()`, and never place an API key in source files, tests, or terminal output.

Model output is untrusted, probabilistic data. Do not use it for authorization, access control, or as a security boundary.

Known configuration errors produce a concise provider-neutral message. Known model request failures produce a concise application error. Low-level exception details are intentionally not shown to terminal users; this does not mean every possible error is caught.

## Extending the application

The separation between the terminal entry point, chat orchestration, and client layer is intended to let a future interface call the application/client layers. This project does not currently include FastAPI or website support.

## Official documentation

- [uv](https://docs.astral.sh/uv/)
- [Groq models](https://console.groq.com/docs/models)
- [Groq model deprecations](https://console.groq.com/docs/deprecations)
- [Pydantic](https://docs.pydantic.dev/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Pydantic AI](https://ai.pydantic.dev/)

## License

This project is licensed under the MIT License. Copyright (c) 2026 Talha Ahmad.
