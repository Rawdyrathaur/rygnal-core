from pathlib import Path


def test_risk_engine_v2_design_doc_exists():
    assert Path("docs/27-risk-engine-v2-design.md").exists()


def test_risk_engine_v2_design_defines_core_concepts():
    content = Path("docs/27-risk-engine-v2-design.md").read_text()

    required_terms = [
        "RiskContext",
        "RiskSignal",
        "RiskSignalRegistry",
        "RiskAssessment",
        "Policy Bridge Direction",
    ]

    for term in required_terms:
        assert term in content


def test_risk_engine_v2_design_keeps_runtime_unchanged():
    content = Path("docs/27-risk-engine-v2-design.md").read_text()

    assert "Do not rewrite the current Risk Engine immediately" in content
    assert "Do not introduce Rust yet" in content
    assert "deterministic, explainable, testable risk architecture" in content
