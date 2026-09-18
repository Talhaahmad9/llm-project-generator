from importlib import resources
from pathlib import Path, PurePosixPath

import pytest

from llm_project_generator.errors import TemplateError
from llm_project_generator.providers import GOOGLE, GROQ
from llm_project_generator import template_store


def test_loading_groq_returns_manifest_union() -> None:
    loaded = template_store.load_template_files(GROQ)

    assert set(loaded) == set(template_store.COMMON_MANIFEST) | set(
        template_store.GROQ_MANIFEST
    )
    assert PurePosixPath(".env.example") in loaded
    assert PurePosixPath(".gitignore") in loaded
    assert PurePosixPath(".env") not in loaded


def test_loading_google_returns_manifest_union() -> None:
    loaded = template_store.load_template_files(GOOGLE)

    assert set(loaded) == set(template_store.COMMON_MANIFEST) | set(
        template_store.GOOGLE_MANIFEST
    )
    assert PurePosixPath(".env.example") in loaded
    assert PurePosixPath(".gitignore") in loaded
    assert PurePosixPath(".env") not in loaded
    assert PurePosixPath("src/app/provider.py") in loaded


def test_duplicate_destination_paths_are_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        template_store,
        "GROQ_MANIFEST",
        (template_store.COMMON_MANIFEST[0],),
    )
    monkeypatch.setitem(
        template_store._PROVIDER_MANIFESTS,
        GROQ.template_name,
        template_store.GROQ_MANIFEST,
    )

    with pytest.raises(TemplateError, match="Duplicate template destination path"):
        template_store.load_template_files(GROQ)


def test_missing_declared_resource_is_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    common = tmp_path / "common"
    overlay = tmp_path / "overlay"
    common.mkdir()
    overlay.mkdir()
    (common / "present").write_bytes(b"ok")
    monkeypatch.setattr(template_store, "_template_root", lambda _name: overlay)

    with pytest.raises(TemplateError, match="Template file is missing"):
        template_store._load_manifest(
            common,
            (PurePosixPath("present"), PurePosixPath("missing")),
            {},
        )


def test_dotenv_manifest_entry_is_rejected() -> None:
    with pytest.raises(TemplateError, match="must not contain .env"):
        template_store._validate_manifest_path(PurePosixPath(".env"))


def test_common_and_groq_overlay_contain_reviewed_assets() -> None:
    root = resources.files("llm_project_generator.project_templates")
    template = root.joinpath("providers", "groq")
    common = root.joinpath("common")

    assert template.is_dir()
    assert (template / ".env.example").is_file()
    assert (common / ".gitignore").is_file()
    assert (common / "LICENSE").is_file()
    assert (template / "pyproject.toml").is_file()
    assert (common / "src" / "app" / "main.py").is_file()
    assert (common / "tests" / "test_main.py").is_file()
    child_names = {child.name for child in template.iterdir()}
    assert ".env" not in child_names
