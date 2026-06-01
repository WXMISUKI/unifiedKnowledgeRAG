## Summary

Add a checksum-aware local BGE-M3 artifact readiness export that sits between Phase 3 promotion review and Phase 6 deployment readiness.

## Phase Alignment

- Roadmap phase: Phase 6 deployment and operations, with explicit Phase 3 bridge value.
- Nature: deployment-adjacent evidence export.
- Non-goal: enabling BGE-M3 as the default embedding provider, changing Qdrant defaults, or changing promotion policy.

## Decisions

- Use the existing BGE-M3 bootstrap artifact layout as the source of truth.
  The local model directory already writes `model-manifest.json`; the readiness report should validate that artifact rather than inventing a second model layout.

- Make checksum coverage explicit.
  The artifact manifest should carry a file inventory and checksum metadata so private-network copies can be compared without guesswork.

- Keep the report read-only and local.
  It should summarize readiness, not download models, not call embedding services, and not change runtime defaults.

- Surface the report in handoff as optional evidence.
  This keeps Phase 6 readiness visible to external control planes without making BGE-M3 promotion automatic.

## Output

- JSON: `docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json`
- Markdown: `docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.md`

## Signals

The report should summarize:

- model path presence
- `model-manifest.json` presence
- required file inventory
- checksum coverage and consistency
- local-files-only posture
- private-network copyability / deployment reuse posture
- deployment-readiness linkage

## Risks / Trade-offs

- Checksums can drift if the artifact is rebuilt or copied incorrectly.
  Mitigation: keep the manifest and readiness report generated from the same local artifact directory.

- The report can be mistaken for runtime promotion.
  Mitigation: make the decision line explicit: keep runtime defaults until evidence is complete.
