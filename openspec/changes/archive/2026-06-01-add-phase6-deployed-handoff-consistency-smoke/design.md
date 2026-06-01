## Summary

Create a compact Phase 6 smoke summary that validates consistency between the deployed field-validation readiness export and the provider handoff bundle.

## Phase Alignment

- Roadmap phase: Phase 6 deployment and operations.
- Nature: documentation-backed smoke evidence.
- Non-goal: runtime default switch.

## Decision Content

- readiness artifact presence
- handoff bundle artifact presence
- readiness row presence in handoff bundle
- status alignment between readiness and bundle summary
- live-url posture alignment

## Decisions

- Keep the smoke read-only and local.
  It should compare already-generated artifacts rather than invoke the deployed provider live.

- Keep the output small and review-friendly.
  The smoke summary should be easy to include in handoff without replacing the underlying readiness or deployed smoke reports.

- Keep the export source paths explicit.
  Every check should point back to the underlying local evidence artifact so reviewers can drill in quickly.

## Risks / Trade-offs

- The smoke can drift if the readiness export or handoff bundle changes without the consistency report being refreshed.
  Mitigation: regenerate the smoke and handoff bundle from the same local evidence flow.

- Integrating the smoke into handoff can widen the bundle slightly.
  Mitigation: make it optional and keep the smoke compact.
