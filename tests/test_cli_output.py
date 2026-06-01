from types import SimpleNamespace

from demo.cli_output import render_outcome, render_run_report, runtime_mode_value


def make_outcome(runtime_metadata="enforce"):
    scenario = SimpleNamespace(
        name="secret-file-access",
        description="Agent attempts to read environment secrets.",
        request=SimpleNamespace(
            tool_name="file_read",
            action="read_file",
            target=".env",
        ),
    )

    result = SimpleNamespace(
        risk_assessment={
            "risk_score": 95,
            "risk_level": "critical",
            "reasons": ["Agent targeted an environment secret file."],
        },
        policy_decision=SimpleNamespace(
            decision="block",
            policy_id="block-env-read",
            reason="Reading environment secret files is not allowed.",
        ),
        execution=SimpleNamespace(
            status="skipped",
        ),
        audit_event=SimpleNamespace(
            event_id="evt_test_123",
            metadata={"runtime_mode": runtime_metadata},
        ),
    )

    return SimpleNamespace(scenario=scenario, result=result)


def test_render_outcome_contains_core_security_fields():
    lines = render_outcome(make_outcome(), index=1)
    output = "\n".join(lines)

    assert "[BLOCK] secret-file-access" in output
    assert "Tool        : file_read" in output
    assert "Action      : read_file" in output
    assert "Target      : .env" in output
    assert "Runtime     : enforce" in output
    assert "Risk        : critical / 95" in output
    assert "Policy      : block-env-read" in output
    assert "Execution   : skipped" in output
    assert "Audit Event : evt_test_123" in output


def test_runtime_mode_uses_audit_metadata_first():
    outcome = make_outcome(runtime_metadata="simulate")

    assert runtime_mode_value(outcome.result) == "simulate"


def test_runtime_mode_falls_back_to_result_model():
    result = SimpleNamespace(
        runtime_mode="observe",
        audit_event=SimpleNamespace(metadata={}),
    )

    assert runtime_mode_value(result) == "observe"


def test_runtime_mode_defaults_to_enforce_when_missing():
    result = SimpleNamespace(
        audit_event=SimpleNamespace(metadata={}),
    )

    assert runtime_mode_value(result) == "enforce"


def test_render_run_report_contains_summary():
    output = render_run_report([make_outcome()])

    assert "Rygnal Real Scenario Runner v1" in output
    assert "Total scenarios: 1" in output
    assert "Audit log: logs/audit_log.jsonl" in output
    assert "Sandbox: demo_sandbox/" in output
