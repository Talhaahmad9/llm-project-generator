<div align="center">

# ⚡ LLM Project Generator

### One command. Four provider templates. Tested chatbot foundations.

[![Python 3.13+](https://img.shields.io/badge/python-3.13%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/llm-project-generator?logo=pypi&logoColor=white)](https://pypi.org/project/llm-project-generator/)
[![CI](https://github.com/Talhaahmad9/llm-project-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/Talhaahmad9/llm-project-generator/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://github.com/Talhaahmad9/llm-project-generator/blob/main/LICENSE)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange)](https://github.com/Talhaahmad9/llm-project-generator)

**Groq · Google Gemini · OpenAI · Anthropic Claude**

Built by **Talha Ahmad**

</div>

## Overview

`llm-project-generator` creates a focused, standalone terminal chatbot project from a packaged provider template. Each generated project combines one provider SDK, Pydantic AI, Pydantic Settings, validated schemas, provider-specific configuration, and deterministic tests around a shared application structure.

It generates one-provider projects; it does not perform runtime multi-provider routing.

## Quick start

Requirements: Python 3.13 or newer and [uv](https://docs.astral.sh/uv/getting-started/installation/).

The shortest path opens an interactive provider menu in a terminal:

```bash
uvx llm-project-generator init my-chatbot
```

For automation, select a provider explicitly. Non-interactive environments require `--provider`:

```bash
uvx llm-project-generator init my-chatbot --provider groq
uvx llm-project-generator init my-chatbot --provider google
uvx llm-project-generator init my-chatbot --provider openai
uvx llm-project-generator init my-chatbot --provider anthropic
```

For a persistent installation:

```bash
uv tool install llm-project-generator
llm-project-generator init my-chatbot
```

Multi-provider generation is available in version `0.2.0` and later.

## Providers

| CLI name | Display name | Environment variable | Default model | Generated dependency | Deterministic verification | Live verification |
| --- | --- | --- | --- | --- | --- | --- |
| `groq` | Groq | `GROQ_API_KEY` | `groq:openai/gpt-oss-120b` | `pydantic-ai-slim[groq]` | Passed | Passed |
| `google` | Google Gemini | `GOOGLE_API_KEY` | `google:gemini-3.5-flash-lite` | `pydantic-ai-slim[google]` | Passed | Passed |
| `openai` | OpenAI | `OPENAI_API_KEY` | `openai:gpt-5.4-mini` | `pydantic-ai-slim[openai]` | Passed | Pending billing |
| `anthropic` | Anthropic Claude | `ANTHROPIC_API_KEY` | `anthropic:claude-sonnet-5` | `pydantic-ai-slim[anthropic]` | Passed | Pending credits |

Deterministic verification covers generation, imports, configuration, mocked provider construction, and shared chatbot behavior. Live verification covers real authentication, model availability, and provider responses. Groq and Google Gemini have completed both so far.

Google Gemini was live-verified with `gemini-3.5-flash-lite` through Google's Free Tier. Free Tier availability and rate limits may vary by project and can change over time.

## Use a generated project

```bash
cd my-chatbot
uv sync
cp .env.example .env
```

Open `.env` in an editor and add the required API key for the provider you selected. `LLM_MODEL` is an optional model override; when it is omitted, the selected provider's default model is used. The generator never requests or copies API keys. The generated `.env` does not exist until you create it and is ignored by Git.

Run the chatbot and its deterministic tests:

```bash
uv run llm-chat
uv run pytest
```

## Features

- Interactive or explicit provider selection.
- Provider-isolated generated dependencies.
- Pydantic validation for settings and chat messages.
- Conversation history within a terminal session.
- Deterministic fake-model and mocked provider tests.
- Safe destination policy with no force, overwrite, or delete behavior.
- Packaged templates available from the installed wheel.
- No generator runtime dependencies.

## Architecture

```text
                         llm-project-generator
                                  |
                    +-------------+-------------+
                    |                           |
          Common chatbot resources      Provider overlay
                    |                           |
                    +-------------+-------------+
                                  |
                         Generated project
                                  |
                  config -> provider -> LLM API
```

Common resources own the terminal loop, chat orchestration, reply execution, schemas, exceptions, and shared tests. Each overlay owns its environment example, README, dependency metadata, provider configuration, provider construction, and provider tests.

## Generated structure

```text
my-chatbot/
|-- .env.example
|-- .gitignore
|-- LICENSE
|-- README.md
|-- pyproject.toml
|-- src/
|   `-- app/
|       |-- __init__.py
|       |-- chat.py
|       |-- client.py
|       |-- config.py
|       |-- exceptions.py
|       |-- main.py
|       |-- provider.py
|       `-- schemas.py
`-- tests/
```

## Safety

The destination parent must already exist, and the destination itself must not exist. Existing files and directories are never overwritten; there is no force or delete behavior.

The generator never creates `.env`, requests API keys, or copies secrets. Generated configuration uses `SecretStr`. Model output is probabilistic and untrusted; it is not an authorization or security boundary.

Automated generated tests use fake models and mocks and do not make real provider requests.

## Project names and destinations

Project names may contain ASCII letters, numbers, dots, underscores, and hyphens. They must begin and end with a letter or number. Runs of dots, underscores, and hyphens are normalized into lowercase hyphens for distribution metadata. The destination parent must exist, and the destination itself must not already exist. A filesystem failure during generation can leave a partial destination; inspect it or remove it before retrying.

## Verification status

The four provider implementations have deterministic generated-suite coverage. Groq and Google Gemini have also completed live verification. OpenAI and Anthropic Claude live checks remain pending billing or credit availability, so this preview does not claim that every provider is production-ready or live-verified.

## Development

```bash
git clone https://github.com/Talhaahmad9/llm-project-generator.git
cd llm-project-generator
uv sync --dev
uv run pytest
uv build --no-sources
```

CI generates and tests all four provider projects without provider credentials.

## Limitations and roadmap

This preview provides a terminal interface only, generates one provider per project, requires Python 3.13+, does not create API keys, does not overwrite existing destinations, and does not make live calls in automated tests. Two live-verification checks are pending.

The next milestones are to complete OpenAI and Anthropic Claude live verification and prepare the criteria for `1.0.0`. Future work such as FastAPI or RAG belongs to separate product milestones; it is not part of the generated chatbot today.

## Contributing

Create a focused branch, run the root tests and build locally, and keep provider resources explicitly allowlisted. Pull requests should preserve deterministic tests and must not add credentials or live API calls.

## Author and license

Built by [Talha Ahmad](https://github.com/Talhaahmad9). Licensed under the [MIT License](https://github.com/Talhaahmad9/llm-project-generator/blob/main/LICENSE).
