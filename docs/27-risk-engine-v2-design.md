# Risk Engine v2 Design

This document defines the direction for Rygnal Risk Engine v2.

## Goal

Risk Engine v2 should become a threat-informed, contextual, explainable risk scoring system for AI-agent tool actions.

The goal is not to replace the current Risk Engine immediately. The goal is to define a clean architecture before changing runtime behavior.

## Current Risk Engine Status

The current Risk Engine is a real MVP. It detects important risky patterns and supports the current Rygnal demo and policy workflow.

However, it is still mostly heuristic and rule-based.

## Why v2 Is Needed

Rygnal should not rely only on simple checks like dangerous command strings or secret-looking file targets.

A stronger risk engine should understand:

- who is requesting the action
- which agent is acting
- which tool is being used
- what action is being requested
- what asset or data is touched
- where data may be sent
- whether the action is reversible
- whether the environment is local, staging, or production
- whether the action is part of a risky chain
- how confident the risk decision is

## Design Principles

- Deterministic first
- Explainable by default
- Policy-compatible
- Testable with fixtures
- Configurable later
- No hidden magic score
- No LLM-only risk decision
- No Rust rewrite in this phase

## Core Concepts

### RiskContext

RiskContext is the normalized input used by the risk engine.

It should include:

- tool_name
- action
- target
- input
- user_id
- agent_id
- environment
- metadata
- runtime_mode later
- policy context later
- recent action history later

### RiskSignal

RiskSignal represents one detected risk reason.

Each signal should include:

- signal_id
- category
- severity
- score
- confidence
- reason
- evidence
- reversible flag when useful

### RiskSignalRegistry

RiskSignalRegistry owns the available detectors.

Examples:

- secret target detector
- sensitive input detector
- dangerous shell detector
- destructive action detector
- external destination detector
- customer data detector
- production environment detector
- suspicious instruction detector

### RiskAssessment

RiskAssessment is the final output.

It should include:

- risk_score
- risk_level
- signals
- reasons
- confidence
- explanation
- recommended_policy_action later

## Risk Layers

Risk Engine v2 should score risk across multiple layers.

| Layer | Purpose |
|---|---|
| Capability risk | How powerful the tool is |
| Action risk | What operation is requested |
| Asset risk | What target or data is touched |
| Data risk | Whether sensitive data is involved |
| Destination risk | Where data may go |
| Environment risk | Local vs staging vs production |
| Reversibility risk | Whether the action can be undone |
| Chain risk | Whether recent actions form an attack pattern |
| Intent risk | Whether prompt/input suggests bypass or exfiltration |

## Scoring Model

Risk Engine v2 should use weighted deterministic scoring.

Example starting thresholds:

| Score | Level |
|---:|---|
| 0-20 | low |
| 21-49 | medium |
| 50-74 | high |
| 75-100 | critical |

Scores should be explainable through signals. Every score increase should map to one or more signals.

## Policy Bridge Direction

Policy Engine should eventually consume risk context cleanly.

Future policy fields may include:

- risk_level
- risk_score_min
- signal_ids_contains
- environment
- runtime_mode

This should happen through a policy-risk bridge, not by forcing unrelated fields into ToolRequest.

## What We Should Not Do Yet

- Do not rewrite the current Risk Engine immediately
- Do not introduce Rust yet
- Do not add LLM-only risk judgment
- Do not add risk_level directly into PolicyRule until evaluation context is designed
- Do not build chain risk before basic RiskContext and RiskSignal models are stable

## Recommended Implementation Phases

### Phase 1: Risk Engine v2 Foundation

- Add RiskContext
- Add RiskSignal
- Add RiskSignalRegistry
- Add deterministic scoring profile
- Keep compatibility with current RiskAssessment output

### Phase 2: Signal Detectors

- Secret target detector
- Sensitive input detector
- Dangerous shell detector
- Destructive action detector
- External destination detector
- Customer data detector
- Production environment detector

### Phase 3: Policy Risk Bridge

- Allow policy engine to evaluate risk context
- Add risk_level policy matching
- Add risk_score_min policy matching
- Keep backward compatibility

### Phase 4: Chain Risk

- Detect read secret then external send
- Detect customer data access then delete
- Detect repeated risky attempts
- Add audit trace correlation

### Phase 5: Future Rust Core Research

- Evaluate whether risk and policy core should move to Rust
- Keep Python SDK stable
- Consider PyO3 only after Python architecture stabilizes

## Decision

Pause direct risk_level and runtime_mode matching in Policy Engine until Risk Engine v2 context is designed.

Continue with deterministic, explainable, testable risk architecture first.
