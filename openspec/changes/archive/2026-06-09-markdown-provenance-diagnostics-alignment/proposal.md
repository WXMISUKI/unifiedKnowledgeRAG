## Why

The current aggregate review on `refund_policy_docs` mixes a real negative-control issue with a page-oriented diagnostics mismatch that comes from treating markdown fixture provenance like paged document provenance. We need a small alignment slice that makes markdown provenance expectations explicit, so chunk-quality review stops over-signaling on non-paged markdown sources and future work stays focused on the actual failure mode.

## What Changes

- Align chunk-quality diagnostics so markdown sources without page-based provenance are not treated as paged-source coverage failures by default.
- Preserve explicit provenance expectations in the report, while keeping runtime retrieval behavior unchanged.
- Refresh local and aggregate golden-case evidence so `refund_policy_docs` review reflects only the remaining real issue after diagnostics alignment.
- Keep the slice evidence-only: no query rewrite, no rerank, no hybrid retrieval, no GraphRAG, and no parser-engine ownership changes.

## Capabilities

### New Capabilities

### Modified Capabilities
- `local-business-rag-golden-cases`: Update chunk-quality diagnostics and reporting so markdown provenance expectations are aligned separately from paged-source coverage checks.
- `provider-roadmap`: Record that provenance diagnostics alignment is a precondition step before any negative-control hardening or advanced retrieval strategy work on markdown sources.

## Impact

- Updates the existing local business golden-case reporting logic and refreshed evidence artifacts.
- Refreshes `docs/local-run/business-rag-golden-cases/real-business-corpus-golden-cases.json` and `.md`.
- Adds focused tests for markdown provenance alignment without affecting paged company-profile behavior.
- Updates roadmap/progress documentation after the evidence refresh.
- No public HTTP API changes.
- No new external dependencies.
- No runtime retrieval default changes.
