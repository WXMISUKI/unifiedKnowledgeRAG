# Phase 11 RAG Retrieve Consumption Smoke

- Report: `phase11-rag-retrieve-consumption-smoke-v1`
- Status: `ready`
- Decision: `keep_caller_consumption_fail_closed`
- Generated At: `2026-06-02T03:13:51.707917+00:00`

## Summary

| Metric | Value |
|---|---|
| total_checks | `3` |
| passed_checks | `3` |
| failed_checks | `0` |

## Checks

| Check | Required | Status | Summary | Recommended Action |
|---|---|---|---|---|
| `phase4_caller_consumption_ready` | `True` | `ready` | phase4_caller_consumption_status=ready | `no_action_required` |
| `provider_contract_smoke_ready` | `True` | `ready` | provider_contract_smoke_passed=true | `no_action_required` |
| `phase10_runtime_boundary_preserved` | `True` | `ready` | runtime_promotion_status=keep_runtime_defaults | `no_action_required` |
