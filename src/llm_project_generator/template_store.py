from __future__ import annotations

from pathlib import PurePosixPath
from typing import TYPE_CHECKING, Mapping
from importlib import resources
from importlib.resources.abc import Traversable

from llm_project_generator.errors import TemplateError
if TYPE_CHECKING:
    from llm_project_generator.providers import ProviderSpec


COMMON_MANIFEST: tuple[PurePosixPath, ...] = (
    PurePosixPath(".gitignore"),
    PurePosixPath("LICENSE"),
    PurePosixPath("src/app/__init__.py"),
    PurePosixPath("src/app/chat.py"),
    PurePosixPath("src/app/client.py"),
    PurePosixPath("src/app/exceptions.py"),
    PurePosixPath("src/app/main.py"),
    PurePosixPath("src/app/schemas.py"),
    PurePosixPath("tests/test_chat.py"),
    PurePosixPath("tests/test_client.py"),
    PurePosixPath("tests/test_main.py"),
    PurePosixPath("tests/test_schemas.py"),
)

GROQ_MANIFEST: tuple[PurePosixPath, ...] = (
    PurePosixPath(".env.example"),
    PurePosixPath("README.md"),
    PurePosixPath("pyproject.toml"),
    PurePosixPath("src/app/config.py"),
    PurePosixPath("src/app/provider.py"),
    PurePosixPath("tests/test_config.py"),
    PurePosixPath("tests/test_provider.py"),
)

GOOGLE_MANIFEST: tuple[PurePosixPath, ...] = (
    PurePosixPath(".env.example"),
    PurePosixPath("README.md"),
    PurePosixPath("pyproject.toml"),
    PurePosixPath("src/app/config.py"),
    PurePosixPath("src/app/provider.py"),
    PurePosixPath("tests/test_config.py"),
    PurePosixPath("tests/test_provider.py"),
)

OPENAI_MANIFEST: tuple[PurePosixPath, ...] = (
    PurePosixPath(".env.example"),
    PurePosixPath("README.md"),
    PurePosixPath("pyproject.toml"),
    PurePosixPath("src/app/config.py"),
    PurePosixPath("src/app/provider.py"),
    PurePosixPath("tests/test_config.py"),
    PurePosixPath("tests/test_provider.py"),
)

_PROVIDER_MANIFESTS: dict[str, tuple[PurePosixPath, ...]] = {
    "providers/groq": GROQ_MANIFEST,
    "providers/google": GOOGLE_MANIFEST,
    "providers/openai": OPENAI_MANIFEST,
}


def _validate_manifest_path(path: PurePosixPath) -> None:
    if path.is_absolute() or ".." in path.parts:
        raise TemplateError(f"Unsafe template path: {path}")
    if path.name == ".env":
        raise TemplateError("The template must not contain .env")


def _template_root(name: str) -> Traversable:
    root = resources.files("llm_project_generator.project_templates").joinpath(*name.split("/"))
    if not root.is_dir():
        raise TemplateError(f"Template not found: {name}")
    return root


def _load_manifest(
    root: Traversable,
    manifest: tuple[PurePosixPath, ...],
    loaded: dict[PurePosixPath, bytes],
) -> None:
    for path in manifest:
        _validate_manifest_path(path)
        if path in loaded:
            raise TemplateError(f"Duplicate template destination path: {path}")
        resource = root.joinpath(*path.parts)
        if not resource.is_file():
            raise TemplateError(f"Template file is missing: {path}")
        try:
            loaded[path] = resource.read_bytes()
        except OSError as exc:
            raise TemplateError(f"Cannot read template file: {path}") from exc


def load_template_files(provider: ProviderSpec) -> Mapping[PurePosixPath, bytes]:
    try:
        provider_manifest = _PROVIDER_MANIFESTS[provider.template_name]
    except KeyError as exc:
        raise TemplateError(
            f"No template manifest is registered for provider: {provider.name}"
        ) from exc

    loaded: dict[PurePosixPath, bytes] = {}
    _load_manifest(_template_root("common"), COMMON_MANIFEST, loaded)
    _load_manifest(_template_root(provider.template_name), provider_manifest, loaded)

    return loaded
