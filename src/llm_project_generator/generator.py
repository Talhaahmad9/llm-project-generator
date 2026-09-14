import re
from pathlib import Path, PurePosixPath

from llm_project_generator.errors import (
    GenerationError,
    InvalidProjectNameError,
    TemplateError,
    UnsafeDestinationError,
)
from llm_project_generator.providers import ProviderSpec
from llm_project_generator.template_store import load_template_files


_PROJECT_NAME = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?")
_SENTINEL = "__PROJECT_DISTRIBUTION_NAME__"


def normalize_project_name(destination: Path) -> str:
    name = destination.name
    if not _PROJECT_NAME.fullmatch(name):
        raise InvalidProjectNameError(f"Invalid project name: {name!r}")
    return re.sub(r"[._-]+", "-", name.lower())


def _validate_destination(destination: Path) -> Path:
    expanded = destination.expanduser()
    parent = expanded.parent
    if not parent.is_dir():
        raise UnsafeDestinationError(
            f"Destination parent is not an existing directory: {parent}"
        )
    if expanded.exists() or expanded.is_symlink():
        raise UnsafeDestinationError(f"Destination already exists: {expanded}")
    return expanded


def _render_files(
    files: dict[PurePosixPath, bytes],
    normalized_name: str,
) -> dict[PurePosixPath, bytes]:
    rendered = dict(files)
    pyproject_path = PurePosixPath("pyproject.toml")
    try:
        pyproject = rendered[pyproject_path]
    except KeyError as exc:
        raise TemplateError("Required template file pyproject.toml is missing") from exc
    try:
        text = pyproject.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise TemplateError("Template pyproject.toml must be strict UTF-8") from exc
    if text.count(_SENTINEL) != 1:
        raise TemplateError("Template project-name sentinel must occur exactly once")
    rendered[pyproject_path] = text.replace(_SENTINEL, normalized_name).encode("utf-8")
    return rendered


def generate_project(destination: Path, provider: ProviderSpec) -> Path:
    expanded = destination.expanduser()
    normalized_name = normalize_project_name(expanded)
    validated_destination = _validate_destination(expanded)
    files = load_template_files(provider)
    rendered = _render_files(dict(files), normalized_name)

    root = validated_destination.resolve(strict=False)
    for relative_path in rendered:
        output = (validated_destination / Path(*relative_path.parts)).resolve(
            strict=False
        )
        if output != root and root not in output.parents:
            raise TemplateError(f"Template output escapes destination: {relative_path}")

    try:
        validated_destination.mkdir()
        for relative_path, content in rendered.items():
            output = validated_destination.joinpath(*relative_path.parts)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(content)
    except OSError as exc:
        raise GenerationError(
            f"Failed writing generated project at {validated_destination}; "
            "partial output may remain"
        ) from exc

    return validated_destination
