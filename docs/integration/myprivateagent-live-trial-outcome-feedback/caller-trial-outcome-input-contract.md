# Caller Trial Outcome Input Contract

## Purpose

This note defines the minimal caller-side JSON contract that `unifiedKnowledgeRAG` expects when exporting Phase 25 live trial outcome feedback.

It is intentionally lightweight:

- the caller owns trial execution
- the caller owns final answer policy
- the caller owns source binding policy
- the provider only consumes the result file to classify provider follow-up posture

## Contract Scope

This contract is only for:

- exporting one caller-side live trial result
- letting the provider classify `no_provider_action_required`, `provider_review_required`, or `provider_blocked`

This contract is not for:

- caller orchestration
- runtime policy
- permissions or approvals
- source-to-agent binding execution
- backend promotion

## Supported Input Shapes

Phase 25 accepts two equivalent input shapes:

- a flat JSON object that directly contains the required fields below
- a MyPrivateAgent repo-side trial outcome JSON object that contains those same fields under `provider_feedback_input`

When `provider_feedback_input` is present and is a JSON object, Phase 25 treats it as the caller feedback payload. This lets callers pass the full MyPrivateAgent trial outcome artifact without manually reconstructing a separate JSON file.

## Required Top-Level Fields

| Field | Type | Meaning |
| --- | --- | --- |
| `live_trial_status` | `string` | Caller-side verdict such as `go`, `review`, or `blocked` |
| `reason_code` | `string` | Compact reason from the caller-side trial |
| `provider_base_url` | `string` | Provider URL used during the trial |
| `agent_id` | `string` | Caller/agent identifier |
| `query` | `string` | The concrete query or representative question used for the trial |
| `provider_retrieve` | `object` | Nested provider retrieve evidence summary |

## Required `provider_retrieve` Fields

| Field | Type | Meaning |
| --- | --- | --- |
| `status` | `string` | Provider retrieve status such as `ready`, `review`, `blocked`, `failed`, or `error` |
| `reason_code` | `string` | Retrieve-side reason code |
| `document_count` | `integer` | Number of retrieved documents exposed to the caller |
| `evidence_pack_status` | `string` | Compact evidence-pack status such as `answerable` or `insufficient_evidence` |
| `citation_policy` | `string` | Expected citation policy, normally `use_only_returned_citations` |
| `allowed_citations` | `array[string]` | Citation allowlist returned by the provider |

## Optional Fields

These fields are useful but not strictly required:

- `domain`
- `blockers`
- `warnings`
- `provider_retrieve.blockers`
- `provider_retrieve.warnings`
- `provider_retrieve.evidence_pack`

## Interpretation Rules

- If the file is missing or invalid JSON, provider feedback is `blocked`.
- If key fields are missing, provider feedback must stay conservative and must not report `no_provider_action_required`.
- If `provider_retrieve.status` is `blocked`, `failed`, or `error`, the provider may classify the result as `provider_blocked`.
- If caller result is `review`, or evidence is `insufficient_evidence`, the provider may classify the result as `provider_review_required`.
- A `go` trial only closes provider follow-up when caller status and provider retrieve evidence are both strong enough.

## Fail-Closed Principle

This contract follows a fail-closed rule:

- weak input should not be treated as provider success
- missing critical fields should remain reviewable or blocked
- the provider should only declare `no_provider_action_required` when the outcome is clear

## Recommended Caller Output Path

The exact path is caller-owned, but the provider expects an explicit path to be passed into:

```powershell
python scripts/export_phase25_myprivateagent_live_trial_outcome_feedback.py `
  --trial-outcome-path "<caller-outcome-json>"
```

## Example

See:

`docs/integration/myprivateagent-live-trial-outcome-feedback/caller-trial-outcome-input-example.json`
