from pathlib import Path
import tomllib

import pytest

from llm_project_generator.errors import (
    InvalidProjectNameError,
    TemplateError,
    UnsafeDestinationError,
)
from llm_project_generator.generator import generate_project, normalize_project_name
from llm_project_generator.providers import GROQ


@pytest.mark.parametrize(
    ("name", "expected"),
    [("My_Project", "my-project"), ("my.project", "my-project"), ("my--project", "my-project")],
)
def test_normalizes_valid_project_names(name: str, expected: str) -> None:
    assert normalize_project_name(Path(name)) == expected


@pytest.mark.parametrize("name", ["my project", "-project", "project-", "", "project\n"])
def test_rejects_invalid_project_names(name: str) -> None:
    with pytest.raises(InvalidProjectNameError):
        normalize_project_name(Path(name))


def test_generates_project_and_renders_name(tmp_path: Path) -> None:
    destination = tmp_path / "My_Project"
    result = generate_project(destination, GROQ)

    assert result == destination
    pyproject = tomllib.loads(
        (destination / "pyproject.toml").read_text(encoding="utf-8")
    )
    assert pyproject["project"]["name"] == "my-project"
    pyproject_text = (destination / "pyproject.toml").read_text(encoding="utf-8")
    assert "__PROJECT_DISTRIBUTION_NAME__" not in pyproject_text
    assert (destination / "src" / "app" / "main.py").is_file()
    assert (destination / "src" / "app" / "client.py").is_file()
    assert (destination / "src" / "app" / "provider.py").is_file()
    assert (destination / "src" / "app" / "config.py").is_file()
    assert (destination / "tests" / "test_main.py").is_file()
    assert (destination / ".env.example").is_file()
    assert (destination / ".gitignore").is_file()
    assert (destination / "LICENSE").is_file()
    assert not (destination / ".env").exists()


@pytest.mark.parametrize("kind", ["file", "directory"])
def test_rejects_existing_destination(tmp_path: Path, kind: str) -> None:
    destination = tmp_path / "existing"
    if kind == "file":
        destination.write_text("x", encoding="utf-8")
    else:
        destination.mkdir()
    with pytest.raises(UnsafeDestinationError):
        generate_project(destination, GROQ)


def test_rejects_missing_parent(tmp_path: Path) -> None:
    with pytest.raises(UnsafeDestinationError):
        generate_project(tmp_path / "missing" / "project", GROQ)


def test_template_validation_precedes_destination_creation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail_template(_provider: object) -> dict[object, bytes]:
        raise TemplateError("invalid template")

    monkeypatch.setattr("llm_project_generator.generator.load_template_files", fail_template)
    destination = tmp_path / "project"
    with pytest.raises(TemplateError):
        generate_project(destination, GROQ)
    assert not destination.exists()
