# Phase 25 Follow-Up Decision Matrix

## Purpose

This matrix is the stage-3 decision entrypoint after a real caller-side trial outcome has already been consumed by Phase 25.

It answers:

`What should we do next after Phase 25?`

## Matrix

| Phase 25 Provider Action | Default Next Action | Reopen Provider Now? | Notes |
| --- | --- | --- | --- |
| `no_provider_action_required` | Keep provider in hold-state | No | The trial did not expose a provider-owned gap. Keep current baseline. |
| `provider_review_required` | Review whether the issue is provider-owned, caller-owned, or corpus-owned | Not by default | Review is a classification step, not immediate reopen. |
| `provider_blocked` | Open a focused provider fix | Yes, narrowly | The trial exposed a provider-side blocker or provider retrieve failure. |

## Detailed Rules

### 1. `no_provider_action_required`

Default action:

- keep current provider baseline
- do not open a new provider feature slice
- continue using the closure summary as the default posture

What to avoid:

- do not reopen query rewrite
- do not reopen rerank
- do not reopen hybrid retrieval
- do not reopen GraphRAG

### 2. `provider_review_required`

Default action:

- review the trial result first
- classify the issue into one of:
  - provider-owned
  - caller-owned
  - corpus-owned

Only reopen provider if:

- the review confirms a provider-owned gap
- or repeated real review evidence forms an accepted failure class

What to avoid:

- do not treat every review result as a provider bug
- do not open advanced strategy work from a single ambiguous review result

### 3. `provider_blocked`

Default action:

- open a focused provider fix
- keep the fix narrow and evidence-driven
- rerun the relevant provider checks after the fix

This is the strongest reopen signal because:

- the trial already exposed a provider-side blocker
- the issue is not just conceptual or review-level

## Suggested Review Questions For `provider_review_required`

Use these questions before reopening provider work:

1. Did the provider fail to return usable evidence?
2. Did the provider return evidence, but the caller failed to use it?
3. Was the issue mainly caused by corpus quality or missing source material?
4. Does the same issue appear across more than one real source?
5. Does the issue justify a focused provider fix or only a future candidate strategy evaluation?

## Boundary Reminder

Even after Phase 25:

- final answer policy stays caller-owned
- source binding policy stays caller-owned
- approvals and audit stay caller/control-plane-owned
- provider should reopen only for provider-owned evidence, retrieval, citation, or source-readiness gaps

## Current Recommended Use

Use this matrix only after:

1. phase 1 access review is complete
2. phase 2 caller trial execution is complete
3. Phase 25 output exists

This matrix is not a substitute for the trial itself.
