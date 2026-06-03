# Phase 11 Source Binding Preview Smoke

- Report: `phase11-source-binding-preview-smoke-v1`
- Status: `ready`
- Decision: `keep_source_binding_preview_only`
- Generated At: `2026-06-02T03:13:51.710359+00:00`

## Summary

| Metric | Value |
|---|---|
| total_checks | `3` |
| passed_checks | `3` |
| failed_checks | `0` |

## Checks

| Check | Required | Status | Summary | Recommended Action |
|---|---|---|---|---|
| `source_binding_summary_ready` | `True` | `ready` | source_binding_status=ready | `no_action_required` |
| `source_binding_policy_owner` | `True` | `ready` | source_binding_policy_owner=caller | `no_action_required` |
| `bindable_source_count_positive` | `True` | `ready` | bindable_sources=2/2 | `no_action_required` |
