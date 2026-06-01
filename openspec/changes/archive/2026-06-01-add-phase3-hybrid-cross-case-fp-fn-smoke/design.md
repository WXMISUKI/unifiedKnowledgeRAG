## Overview

This change adds a read-only Phase 3 cross-case smoke report focused on hybrid-related FP/FN risk visibility. The smoke does not execute retrieval backends. It verifies that existing exported evidence still captures expected risk signals.

## Inputs

- Baseline benchmark evidence:
  `docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.json`
- FP/FN review evidence:
  `docs/benchmark/chinese-seed/fp-fn-review/phase3-fp-fn-review.json`
- Candidate evaluation protocol document:
  `docs/benchmark/chinese-seed/retrieval-candidate-evaluation-protocol/phase3-retrieval-candidate-evaluation-protocol.md`

## Smoke Checks

1. Cross-case risk-case coverage exists in baseline evidence.
2. Expected false-positive trap cases are captured in FP/FN review evidence.
3. Identifier-noise and policy-nuance positive controls are still successful in baseline evidence.
4. Candidate evaluation protocol artifact exists for reviewer context.

## Status Rule

- `ready` when all checks pass.
- `blocked` when one or more checks fail.

This status is evidence-health status, not promotion status.

## Non-Goals

- No runtime retrieval execution.
- No candidate promotion.
- No threshold changes.
- No API changes.
