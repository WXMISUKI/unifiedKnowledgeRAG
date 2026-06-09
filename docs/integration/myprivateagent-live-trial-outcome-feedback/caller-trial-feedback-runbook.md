# Caller Trial Feedback Runbook

## Purpose

This runbook is the execution entrypoint after provider closure.

It answers:

`After the RAG provider is closed and held stable, what do we do next?`

The answer is:

`Run a real caller-side trial, export the outcome, and let provider-side feedback decide whether anything should reopen.`

## Stage Split

The post-closure workflow should be treated as three ordered stages:

### Stage 1. Caller Trial Access

Goal:

- confirm the caller can use the provider through the current access path

Primary artifacts:

- Phase 15 dispatch package
- Phase 16 minimal access loop

### Stage 2. Caller Trial Outcome Export

Goal:

- export a real caller-side trial result in the agreed JSON shape

Primary artifacts:

- caller trial outcome input contract
- caller trial outcome example JSON

### Stage 3. Provider Feedback Consumption

Goal:

- let the provider classify whether follow-up is required

Primary artifact:

- Phase 25 live trial outcome feedback

## Ordered Steps

### Step 1. Review dispatch readiness

Read:

- `docs/integration/myprivateagent-repo-side-trial-dispatch/phase15-myprivateagent-repo-side-trial-dispatch-package.md`

Confirm:

- dispatch state is ready
- caller checklist is visible
- no provider-side primitive blocker remains

### Step 2. Review minimal access loop

Read:

- `docs/integration/myprivateagent-minimal-access-loop/phase16-myprivateagent-minimal-access-loop.md`

Confirm:

- access loop state is ready
- the caller checklist still says trial can begin
- remaining review items are context-only, not blockers

### Step 3. Execute the real caller-side trial

This step happens in the caller repository, not here.

Boundary:

- caller executes the trial
- caller owns final answer policy
- caller owns trial orchestration
- provider does not participate in execution

### Step 4. Export the trial outcome JSON

Use:

- `docs/integration/myprivateagent-live-trial-outcome-feedback/caller-trial-outcome-input-contract.md`
- `docs/integration/myprivateagent-live-trial-outcome-feedback/caller-trial-outcome-input-example.json`

Minimum expectation:

- top-level caller verdict
- provider retrieve status
- evidence-pack status
- citation policy
- allowed citations

### Step 5. Run provider-side Phase 25 feedback export

Command:

```powershell
python scripts/export_phase25_myprivateagent_live_trial_outcome_feedback.py `
  --trial-outcome-path "<caller-outcome-json>"
```

Output:

- `docs/integration/myprivateagent-live-trial-outcome-feedback/phase25-myprivateagent-live-trial-outcome-feedback.json`
- `docs/integration/myprivateagent-live-trial-outcome-feedback/phase25-myprivateagent-live-trial-outcome-feedback.md`

### Step 6. Make the next decision from Phase 25

If Phase 25 returns:

- `no_provider_action_required`
  - keep provider in hold-state
- `provider_review_required`
  - review whether the issue is provider-owned, corpus-owned, or caller-owned
- `provider_blocked`
  - open a focused provider fix

## Decision Rule

Do not reopen provider-side feature work because the trial merely exists.

Only reopen if Phase 25 or follow-up review confirms:

- a provider-owned blocked issue
- a provider-owned repeated review issue
- a stronger trigger defined in the closure summary

## Current Recommended Use

At the current stage, this runbook is the default path after provider closure.

That means:

1. do not open new provider features first
2. do not start advanced RAG strategy work first
3. do the real caller trial first
4. let real feedback choose the next slice
