"""Shared data models for Rygnal."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class Decision(StrEnum):
    """Possible policy decisions."""

    ALLOW = "allow"
    BLOCK = "block"
    REQUIRE_APPROVAL = "require_approval"
    SIMULATE = "simulate"


class Severity(StrEnum):
    """Risk severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ToolRequest(BaseModel):
    """A tool action requested by an AI agent."""

    tool_name: str
    action: str | None = None
    target: str | None = None
    input: Any | None = None
    user_id: str = "demo_user"
    agent_id: str = "demo_agent"
    environment: str = "local"
    metadata: dict[str, Any] = Field(default_factory=dict)


class PolicyRule(BaseModel):
    """A single policy rule."""

    id: str
    decision: Decision
    severity: Severity = Severity.LOW
    reason: str

    tool_name: str | None = None
    action: str | None = None
    environment: str | None = None
    target_contains: str | None = None
    input_contains: str | None = None


class PolicyDecision(BaseModel):
    """Policy evaluation result."""

    decision: Decision
    allowed: bool
    severity: Severity
    reason: str
    policy_id: str | None = None
