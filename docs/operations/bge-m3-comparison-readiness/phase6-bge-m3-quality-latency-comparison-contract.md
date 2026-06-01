# Phase 6 BGE-M3 Quality/Latency Comparison Contract

## Scope

- Phase: `Phase 6 / Deployment And Operations` with `Phase 3 promotion bridge`
- Type: read-only comparison contract
- Goal: define reproducible evidence rules for comparing BGE-M3 candidate behavior with current mock/fixture baseline

## Non-goals

- Do not switch runtime embedding provider to BGE-M3 by default.
- Do not switch runtime retrieval backend to Qdrant or hybrid by default.
- Do not download models, rebuild indexes, run deployment automation, or execute control-plane policy.

## Required Evidence Classes

### 1) Baseline Evidence

- Current mock/fixture benchmark baseline exists and is machine-readable.
- Baseline includes quality metrics: `hit_rate`, `citation_match_rate`, `empty_handling_rate`.
- Baseline includes latency profile at least with `average`, `median`, and `p95` latency.

Recommended action when missing: `regenerate_mock_fixture_baseline`.

### 2) BGE-M3 Candidate Evidence

- Candidate benchmark evidence exists for BGE-M3 local path (or explicitly documents missing state as review).
- Candidate includes same metric schema as baseline for direct comparison.
- Candidate evidence timestamps and source fixture scope are recorded.

Recommended action when missing: `regenerate_bge_m3_candidate_evidence`.

### 3) Artifact/Deployment Linkage

- BGE-M3 artifact readiness report exists and is parseable.
- Deployment readiness and runtime diagnostics evidence are linked in the same review cycle.
- Local-files-only and private-network copy posture are visible.

Recommended action when missing: `refresh_artifact_and_deployment_linkage`.

### 4) Risk Controls

- FP/FN review evidence is present or explicitly marked as open review gate.
- Empty-case and negative-control behavior are visible for candidate interpretation.
- Deployed smoke remains optional in local phase, but absence must stay explicit.

Recommended action when missing: `refresh_fp_fn_and_negative_control_evidence`.

## Readiness States

- `ready`: all comparison evidence classes are present and internally consistent.
- `review`: evidence exists but open gates remain, or candidate artifacts are partial.
- `blocked`: critical comparison artifacts are missing or contradictory.

## Decision Boundary

Comparison contract output is a prerequisite artifact for promotion review. It is not a promotion decision. Until separate promotion gates are closed, keep `decision=keep_runtime_defaults`.
