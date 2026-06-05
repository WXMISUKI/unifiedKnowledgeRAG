# Provider Source Binding Summary

- Report: `provider-source-binding-summary-v1`
- Status: `ready`
- Generated At: `2026-06-05T01:54:01.915851+00:00`
- Provider: `unifiedKnowledgeProvider`
- Contract: `knowledge-provider-contract-v1`
- Total Sources: `2`
- Bindable Sources: `2`
- Status Counts: `ready=2`
- Recommended Action Counts: `bind_source_from_control_plane=2`

## Sources

| Source | Status | Bindable | Domain | Language | Sensitivity | Formats | Citation Granularity | Backend | Index | Documents | Citations | Chunks | Parser Ready | Unsupported | Drift | Preflight | Recommended Action |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| `refund_policy_docs` | `ready` | `True` | `after_sales_policy` | `zh-CN` | `internal` | `markdown` | `section` | `ready` | `ready` | 1 | 7 | 7 | 1 | 0 | `in_sync` | `ready` | `bind_source_from_control_plane` |
| `logistics_faq` | `ready` | `True` | `logistics_support` | `zh-CN` | `internal` | `markdown` | `section` | `ready` | `ready` | 1 | 6 | 6 | 1 | 0 | `in_sync` | `ready` | `bind_source_from_control_plane` |

## Operation Notes

- This summary is read-only and does not create source-to-agent bindings.
- External control planes own binding policy, approvals, audit, and final answer workflow.
- Detailed document diagnostics remain available from source document manifests and ingestion preflight endpoints.
