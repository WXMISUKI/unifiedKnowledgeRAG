## Overview

This change adds a lightweight Phase 3 smoke that compresses existing multi-chunk aggregation evidence and relation-aware grading evidence into one readable review artifact.

## Decisions

- Reuse the already-exported local benchmark evidence files instead of introducing new retrieval execution paths.
- Treat the smoke as optional review evidence, not as a promotion gate.
- Keep the report read-only and local.
- Preserve runtime defaults and caller ownership boundaries.

## Report Shape

- Report id, status, decision, generated timestamp.
- Summary counts for total checks, passed checks, and failed checks.
- Source paths for aggregation candidate evidence, negative-control evidence, and relation-aware grading evidence.
- Per-check status rows for the positive split-chunk control, the negative control, and relation-aware grading alignment.

## Non-Goals

- No new retrieval backend logic.
- No new graph execution.
- No runtime aggregation promotion.
- No caller policy changes.
