## Context

Operators now have:

- a readiness report
- an operator guide
- a config reference

The missing piece is a single ordered path that turns those documents into an execution flow.

## Goals / Non-Goals

**Goals**

- Make the deployment preparation flow explicit and sequential.
- Keep the runbook short and directly actionable.
- Tie the runbook to existing commands and docs.

**Non-Goals**

- No runtime changes.
- No deployment automation.
- No change to readiness semantics.

## Decisions

- Structure the runbook around phases: inspect, configure, refresh, verify, and optionally smoke.
- Use current evidence files as checkpoints.
- End with a clear handoff rule: current evidence is the source of truth after refresh.

## Risks / Trade-offs

- A runbook can drift if docs move; keep it shallow and link back to the operator guide and config reference.
- Too much detail would turn it into a policy page; keep it focused on the path to deployment.
