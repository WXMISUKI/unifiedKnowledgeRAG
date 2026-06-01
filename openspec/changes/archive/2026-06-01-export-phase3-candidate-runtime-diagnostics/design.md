## Overview

This change introduces a read-only Phase 3 runtime diagnostics report focused on candidate promotion prerequisites. The report is intentionally local and lightweight. It complements existing promotion readiness exports by explicitly describing runtime-adjacent gaps that still keep promotion in review.

## Data Inputs

- Runtime settings from `app/config.py`.
- Local model artifact path diagnostics from configured embedding model path.
- Existing Phase 3 readiness export presence/status.
- Optional deployed smoke evidence presence/status.

## Report Shape

- `id`, `generated_at`, `status`, `decision`.
- `summary` with total/ready/review/blocked prerequisite counts and open prerequisite ids.
- `runtime_config` with non-secret configuration snapshot.
- `model_artifacts` with local artifact diagnostics.
- `prerequisites` as a stable list of per-check status rows.
- `notes` explaining boundary and non-goals.

## Status Rules

- `blocked`: any prerequisite row is blocked.
- `review`: no blocked rows and at least one review row.
- `ready`: all rows are ready.

Expected local baseline stays `review`.

## Non-Goals

- No backend switching.
- No model downloads.
- No Qdrant calls.
- No GraphRAG execution.
- No runtime promotion changes.
