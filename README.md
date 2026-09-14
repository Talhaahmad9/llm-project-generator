# llm-project-generator

`llm-project-generator` creates a ready-to-run LLM chatbot project from a reviewed, packaged template.

## Current status

V1 supports only Groq. Groq is included because this template has been live verified. Other providers are not advertised or generated yet.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)

The generator itself has no runtime dependencies. It uses the standard Python library and includes its template assets in the installed package.

## Use from a clone

From the repository root:

```bash
uv sync --dev
uv run llm-project-generator --help
uv run llm-project-generator init <destination> --provider groq
```

For example:

```bash
uv run llm-project-generator init my-chatbot --provider groq
```

The package is not currently published on PyPI. A locally built wheel can be run with `uvx` when needed by passing the wheel path to `uvx`.

## What it creates

The command creates a new destination containing the reviewed Groq chatbot:

```text
.env.example
.gitignore
README.md
pyproject.toml
src/app/
tests/
```

The generated project keeps the `app` Python package, deterministic fake-model tests, the `llm-chat` console entry point, and the default model `groq:openai/gpt-oss-120b`.

## Run a generated chatbot

Enter the generated project and install its dependencies:

```bash
cd <destination>
uv sync
cp .env.example .env
```

Edit `.env` and add your own `GROQ_API_KEY`. `LLM_MODEL` is optional and can override the default model. Then start the chatbot:

```bash
uv run llm-chat
```

`.env.example` is generated as a placeholder. `.env` is excluded by the template's `.gitignore` and is never generated or copied by this project. Never put a real key in source control.

## Project names and destinations

The distribution name comes from the destination directory name. Names may contain ASCII letters, numbers, periods, underscores, and hyphens; they must begin and end with a letter or number. Spaces and invalid boundary characters are rejected. Period, underscore, and hyphen runs are normalized to one lowercase hyphen: `My_Project` becomes `my-project`.

The destination's parent directory must already exist. The destination itself must not exist, even if it is empty. Existing files and directories are never overwritten, and V1 has no force or delete behavior. An operating-system write failure may leave partial output in the destination.

## Development and testing

Install development dependencies and run the root test suite with:

```bash
uv sync --dev
uv run pytest
```

The root tests exercise provider resolution, resource loading, generation, and CLI behavior. The chatbot tests are packaged template assets; they are not collected from their packaged location by the generator's root test suite.

## Layout

```text
src/llm_project_generator/                    generator package
src/llm_project_generator/project_templates/  packaged template assets
tests/                                        generator tests
```

## Security

The generator does not request, create, inspect, or copy API keys. It creates only `.env.example`; users supply their own secret in a local `.env`, which is excluded from version control.

The generator and generated application use deterministic validation, configuration, file selection, and error handling. LLM responses are probabilistic output from the selected provider and should not be treated as deterministic application logic or as a security boundary.

## Limitations

V1 generates only the live-verified Groq chatbot. It does not generate other providers, overwrite existing destinations, delete output, run `uv sync` for the user, or execute the generated chatbot's tests. Licensing has not yet been finalized; the repository's `LICENSE` file is currently empty.

## Further reading

- [uv documentation](https://docs.astral.sh/uv/)
- [Groq documentation](https://console.groq.com/docs)
- [Pydantic AI documentation](https://ai.pydantic.dev/)
