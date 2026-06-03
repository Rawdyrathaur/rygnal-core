# MCP Tool-Call Adapter Prototype

This prototype proves that an MCP-style tool call payload can be routed through Rygnal before execution.

## Goal

Protect MCP-style tool calls with Rygnal policy, risk scoring, audit logging, and safe execution behavior.

## What This Includes

- MCP-style tools/call adapter
- Conversion from MCP payload to Rygnal ToolRequest
- Safe file read allowed through Rygnal
- Secret file read blocked through Rygnal
- Audit event generated for each tool call
- Tests that run without a live MCP server

## Why No Live MCP Server Yet

This prototype focuses on the protection boundary first.

It proves that MCP-style tool call payloads can be normalized into Rygnal ToolRequest objects and evaluated before execution.

A live MCP server/client integration should be added separately after this adapter contract is stable.

## Run Tests

pytest -q tests/test_mcp_tool_call_adapter.py

## Security Notes

- Do not execute MCP tool calls directly
- Convert MCP payloads into ToolRequest first
- Route every protected MCP tool call through Rygnal
- Audit every protected tool call
- Keep live MCP server integration separate and optional for now

## Future Work

- Add live MCP client/server example
- Add stricter MCP schema validation
- Add multi-tool call handling
- Add MCP approval workflow examples
- Add MCP gateway research
