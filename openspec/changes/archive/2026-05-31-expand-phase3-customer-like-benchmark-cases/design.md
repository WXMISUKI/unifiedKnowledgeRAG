## Context

Phase 3 decisions are evidence-gated. The current seed set covers many categories, but promotion-risk scenarios still need stronger customer-like traps where retrieval may over-return or miss subtle policy boundaries.

We should expand fixtures with minimal scope: enough to improve signal, small enough to keep test determinism and iteration speed.

## Goals / Non-Goals

**Goals:**

- Add a bounded set of customer-like benchmark cases for gate confidence.
- Preserve deterministic local execution and existing benchmark export workflows.
- Improve visibility of false-positive and false-negative behavior by category.

**Non-Goals:**

- Changing retrieval runtime defaults.
- Introducing new retrievers, rerankers, or GraphRAG execution.
- Modifying provider HTTP contracts.
- Treating fixture expansion as production promotion.

## Decisions

- Keep existing baseline fixture file and append new cases with stable ids.
  This avoids creating parallel fixture complexity while preserving reproducible reports.

- Focus new cases on gate-risk categories.
  Priority categories are expected-empty overlap traps, noisy identifiers, and policy nuance phrasing.

- Update tests that currently assert fixed case counts.
  Assertions should remain explicit and intentional after fixture expansion.

## Risks / Trade-offs

- More cases can increase test runtime -> keep addition small and focused.
- Expanded fixture may expose more candidate weaknesses -> treat as desired signal, not regression.
- Historical report comparability changes -> note the fixture version change in evidence notes when exporting.
