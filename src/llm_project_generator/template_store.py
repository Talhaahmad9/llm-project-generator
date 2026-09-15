from pathlib import PurePosixPath
from typing import Mapping
from importlib import resources
from importlib.resources.abc import Traversable

from llm_project_generator.errors import TemplateError
from llm_project_generator.providers import ProviderSpec


TEMPLATE_MANIFEST: tuple[PurePosixPath, ...] = (
    PurePosixPath(".env.example"),
    PurePosixPath(".gitignore"),
    PurePosixPath("LICENSE"),
    PurePosixPath("README.md"),
    PurePosixPath("pyproject.toml"),
    PurePosixPath("src/app/__init__.py"),
    PurePosixPath("src/app/chat.py"),
    PurePosixPath("src/app/client.py"),
    PurePosixPath("src/app/config.py"),
    PurePosixPath("src/app/exceptions.py"),
    PurePosixPath("src/app/main.py"),
    PurePosixPath("src/app/schemas.py"),
    PurePosixPath("tests/test_chat.py"),
    PurePosixPath("tests/test_client.py"),
    PurePosixPath("tests/test_config.py"),
    PurePosixPath("tests/test_main.py"),
    PurePosixPath("tests/test_schemas.py"),
)


def _validate_manifest_path(path: PurePosixPath) -> None:
    if path.is_absolute() or ".." in path.parts:
        raise TemplateError(f"Unsafe template path: {path}")
    if path.name == ".env":
        raise TemplateError("The template must not contain .env")


def _template_root(provider: ProviderSpec) -> Traversable:
    root = resources.files("llm_project_generator.project_templates").joinpath(
        provider.template_name
    )
    if not root.is_dir():
        raise TemplateError(f"Template not found: {provider.template_name}")
    return root


def load_template_files(provider: ProviderSpec) -> Mapping[PurePosixPath, bytes]:
    root = _template_root(provider)
    loaded: dict[PurePosixPath, bytes] = {}

    for path in TEMPLATE_MANIFEST:
        _validate_manifest_path(path)
        resource = root.joinpath(*path.parts)
        if not resource.is_file():
            raise TemplateError(f"Template file is missing: {path}")
        try:
            loaded[path] = resource.read_bytes()
        except OSError as exc:
            raise TemplateError(f"Cannot read template file: {path}") from exc

    return loaded
