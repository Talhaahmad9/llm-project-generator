from importlib import resources


def test_groq_chatbot_template_contains_reviewed_assets() -> None:
    template = resources.files("llm_project_generator.project_templates").joinpath(
        "groq_chatbot"
    )

    assert template.is_dir()
    assert (template / ".env.example").is_file()
    assert (template / ".gitignore").is_file()
    assert (template / "LICENSE").is_file()
    assert (template / "pyproject.toml").is_file()
    assert (template / "src" / "app" / "main.py").is_file()
    assert (template / "tests" / "test_main.py").is_file()
    child_names = {child.name for child in template.iterdir()}
    assert ".env" not in child_names
