from pathlib import Path


def test_release_readiness_doc_exists():
    doc = Path("docs/release-readiness-v0.1.md")
    assert doc.exists()


def test_release_readiness_doc_has_required_sections():
    content = Path("docs/release-readiness-v0.1.md").read_text()

    required_sections = [
        "Release Readiness",
        "Required Validation",
        "Docker",
        "Included",
        "Not Included",
        "Known Limitations",
        "Release",
    ]

    for section in required_sections:
        assert section.lower() in content.lower()


def test_release_notes_draft_exists_and_is_honest_about_scope():
    doc = Path("docs/release-notes-v0.1-draft.md")
    assert doc.exists()

    content = doc.read_text()

    assert "v0.1-core-mvp" in content
    assert "local-first core MVP" in content
    assert "full SaaS product" in content
    assert "real AI-agent framework integration" in content


def test_release_docs_include_validation_commands():
    content = Path("docs/release-readiness-v0.1.md").read_text()

    required_commands = [
        "ruff format src tests demo",
        "ruff check src tests demo",
        "pytest -q",
        "bandit -r src demo -c pyproject.toml",
        "pip-audit -r requirements-dev.txt",
        "python -m demo.run_demo",
    ]

    for command in required_commands:
        assert command in content
