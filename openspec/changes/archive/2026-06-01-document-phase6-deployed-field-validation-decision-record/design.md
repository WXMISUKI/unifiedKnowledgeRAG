## Summary

Create a lightweight decision record that freezes the current Phase 6 deployed field-validation verdict and open gates.

## Phase Alignment

- Roadmap phase: Phase 6 deployment and operations.
- Nature: documentation-only decision trace.
- Non-goal: runtime default switch.

## Decision Content

- current verdict (`keep_local_review_until_deployed_smoke`)
- review state (`review`)
- open gate list
- next-step entry criteria for live URL validation

## Decisions

- Keep the record documentation-only and local.
  It should summarize the current posture rather than execute any deployed validation or change runtime defaults.

- Keep the output compact and review-friendly.
  The decision record should be easy to reference from handoff without replacing the readiness or smoke artifacts.

- Keep the evidence basis explicit.
  Every statement should point back to the readiness export, consistency smoke, and existing handoff evidence chain.

## Risks / Trade-offs

- The decision record can drift if readiness or bundle evidence changes without being refreshed.
  Mitigation: regenerate the record after readiness or handoff evidence changes.

- A concise record can omit nuance.
  Mitigation: include the current open gates and next-step criteria so the boundary remains explicit.
