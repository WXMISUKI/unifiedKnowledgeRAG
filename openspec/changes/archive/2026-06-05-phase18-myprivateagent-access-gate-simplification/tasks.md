## 1. Specification

- [x] 1.1 Create proposal, design, and provider-roadmap delta spec for the Phase 18 access gate simplification.
- [x] 1.2 Validate the OpenSpec change before implementation.

## 2. Implementation

- [x] 2.1 Add a shared MyPrivateAgent access gate helper that separates primitive access signals from review context.
- [x] 2.2 Update provider handoff bundle and handoff refresh access-focused visibility to use the simplified gate.
- [x] 2.3 Update Phase 14/15/16 blocker classification and caller checklist generation to consume the simplified gate.
- [x] 2.4 Refresh generated Phase 14/15/16 and provider handoff evidence artifacts.
- [x] 2.5 Update roadmap and progress tracker with the Phase 18 decision boundary.

## 3. Verification

- [x] 3.1 Add or update focused tests for ready primitive access gates with review-only context.
- [x] 3.2 Run focused pytest coverage for handoff and Phase 14/15/16 access classification.
- [x] 3.3 Run `openspec validate --all --strict`.

## 4. Archive

- [x] 4.1 Mark all tasks complete after verification.
- [x] 4.2 Archive `phase18-myprivateagent-access-gate-simplification`.
