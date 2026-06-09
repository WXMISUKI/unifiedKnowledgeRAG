# Caller Trial Execution Task Pack

## Purpose

This task pack turns stage 2 of the post-closure workflow into concrete execution tasks.

It is meant to be used before switching into the caller repository.

## Stage-2 Goal

The goal is not to improve the provider.

The goal is:

- execute one real caller-side trial
- capture a reliable outcome
- export the result in provider-consumable form

## Before Trial

### Required Checks

1. Review Phase 15 dispatch package
2. Review Phase 16 minimal access loop
3. Confirm provider URL is known
4. Confirm target source/question scope is clear
5. Confirm trial will preserve returned citations instead of free-form answer shaping

### Not Blockers By Default

The following may remain `review` context without blocking the trial by default:

- broader provider handoff review context
- candidate backend review context
- runtime promotion review context

## Trial Target

The minimum target for one caller-side real trial is:

1. send one or more realistic business questions through the caller path
2. preserve provider retrieve evidence
3. observe whether returned citations are usable
4. determine whether the caller can complete its own grounded-answer path

## During Trial

Record at least:

- query
- provider base URL
- agent id or caller id
- caller-side verdict: `go`, `review`, or `blocked`
- provider retrieve status
- provider retrieve reason code
- document count
- evidence-pack status
- citation policy
- allowed citations

Recommended extra notes:

- whether citations were sufficient for the caller
- whether the caller had to add extra fallback behavior
- whether the issue looked provider-owned or caller-owned

## Required Output

The required output is one outcome JSON matching:

- `docs/integration/myprivateagent-live-trial-outcome-feedback/caller-trial-outcome-input-contract.md`

Recommended starting point:

- `docs/integration/myprivateagent-live-trial-outcome-feedback/caller-trial-outcome-input-example.json`

## After Trial

### Provider-Side Handoff

Return the explicit outcome JSON path to this repository and run:

```powershell
python scripts/export_phase25_myprivateagent_live_trial_outcome_feedback.py `
  --trial-outcome-path "<caller-outcome-json>"
```

### Expected Decision

The expected follow-up is one of:

- `no_provider_action_required`
- `provider_review_required`
- `provider_blocked`

## Done Criteria

Stage 2 is complete when:

1. at least one real caller-side trial has executed
2. one explicit outcome JSON file exists
3. the outcome can be consumed by Phase 25
4. the provider can classify the follow-up posture from real feedback

## What Not To Do

Do not treat stage 2 as a provider feature phase.

That means:

- do not reopen query rewrite first
- do not reopen rerank first
- do not reopen hybrid retrieval first
- do not reopen GraphRAG first
- do not extend provider internals before a real outcome exists
