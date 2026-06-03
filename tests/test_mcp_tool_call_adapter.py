from pathlib import Path

from examples.mcp_tool_call_adapter import build_demo_rygnal, handle_mcp_tool_call


def test_mcp_style_tool_call_allows_safe_file_read(tmp_path):
    audit_log_path = tmp_path / "audit_log.jsonl"
    rygnal = build_demo_rygnal(str(audit_log_path))

    payload = {
        "jsonrpc": "2.0",
        "id": "mcp_safe_read",
        "method": "tools/call",
        "params": {
            "name": "file_read",
            "arguments": {
                "action": "read_file",
                "target": "README.md",
            },
        },
    }

    result = handle_mcp_tool_call(payload, rygnal)

    assert result["id"] == "mcp_safe_read"
    assert result["allowed"] is True
    assert result["executed"] is True
    assert result["decision"] == "allow"
    assert result["execution_status"] == "executed"
    assert result["risk_level"] == "low"
    assert result["audit_event_id"]
    assert result["result"]["target"] == "README.md"
    assert Path(audit_log_path).exists()


def test_mcp_style_tool_call_blocks_secret_file_read(tmp_path):
    audit_log_path = tmp_path / "audit_log.jsonl"
    rygnal = build_demo_rygnal(str(audit_log_path))

    payload = {
        "jsonrpc": "2.0",
        "id": "mcp_secret_read",
        "method": "tools/call",
        "params": {
            "name": "file_read",
            "arguments": {
                "action": "read_file",
                "target": ".env",
            },
        },
    }

    result = handle_mcp_tool_call(payload, rygnal)

    assert result["id"] == "mcp_secret_read"
    assert result["allowed"] is False
    assert result["executed"] is False
    assert result["decision"] == "block"
    assert result["execution_status"] == "skipped"
    assert result["risk_level"] == "critical"
    assert result["audit_event_id"]
    assert result["result"] is None
    assert Path(audit_log_path).exists()


def test_mcp_style_tool_call_handles_missing_arguments(tmp_path):
    audit_log_path = tmp_path / "audit_log.jsonl"
    rygnal = build_demo_rygnal(str(audit_log_path))

    payload = {
        "jsonrpc": "2.0",
        "id": "mcp_missing_args",
        "method": "tools/call",
        "params": {
            "name": "file_read",
        },
    }

    result = handle_mcp_tool_call(payload, rygnal)

    assert result["id"] == "mcp_missing_args"
    assert result["audit_event_id"]
    assert Path(audit_log_path).exists()
