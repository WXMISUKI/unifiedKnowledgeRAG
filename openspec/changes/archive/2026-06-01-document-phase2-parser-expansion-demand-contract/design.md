## Summary

Create a lightweight contract document that defines when parser expansion should be considered beyond the current Markdown baseline.

## Phase Alignment

- Roadmap phase: Phase 2 enterprise document ingestion baseline.
- Nature: documentation-only governance contract.
- Non-goal: parser dependency onboarding, ingestion execution changes, or runtime default switching.

## Contract Content

- Baseline boundary:
  - Markdown remains the default parser baseline.
  - Non-Markdown formats remain deferred unless evidence requires expansion.
- Demand evidence classes:
  - source format demand from source package metadata
  - unsupported document distribution from ingestion preflight/source binding evidence
  - parser-ready vs unsupported trend visibility across corpus snapshots
- Gate expectations:
  - explicit false-positive/false-negative parser quality review plan for each candidate parser family
  - latency/resource/deployment impact review before promotion
  - no automatic parser promotion from local evidence-only artifacts

## Verification

- `openspec validate document-phase2-parser-expansion-demand-contract --strict`
