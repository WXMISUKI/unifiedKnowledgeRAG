# Provider Source Binding Summary

- Report: `provider-source-binding-summary-v1`
- Status: `ready`
- Generated At: `2026-06-13T13:10:48.433068+00:00`
- Provider: `unifiedKnowledgeProvider`
- Contract: `knowledge-provider-contract-v1`
- Total Sources: `6`
- Bindable Sources: `6`
- Status Counts: `ready=6`
- Recommended Action Counts: `bind_source_from_control_plane=6`

## Sources

| Source | Status | Bindable | Domain | Language | Sensitivity | Formats | Citation Granularity | Backend | Index | Documents | Citations | Chunks | Parser Ready | Unsupported | Drift | Preflight | Recommended Action |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| `refund_policy_docs` | `ready` | `True` | `after_sales_policy` | `zh-CN` | `internal` | `markdown` | `section` | `ready` | `ready` | 1 | 7 | 7 | 1 | 0 | `in_sync` | `ready` | `bind_source_from_control_plane` |
| `logistics_faq` | `ready` | `True` | `logistics_support` | `zh-CN` | `internal` | `markdown` | `section` | `ready` | `ready` | 1 | 6 | 6 | 1 | 0 | `in_sync` | `ready` | `bind_source_from_control_plane` |
| `split_refund_policy_docs` | `ready` | `True` | `general` | `unknown` | `internal` | `markdown` | `section` | `ready` | `ready` | 1 | 2 | 2 | 1 | 0 | `in_sync` | `ready` | `bind_source_from_control_plane` |
| `invoice_policy_faq` | `ready` | `True` | `invoice_policy_support` | `zh-CN` | `internal` | `markdown` | `section` | `ready` | `ready` | 1 | 3 | 3 | 1 | 0 | `in_sync` | `ready` | `bind_source_from_control_plane` |
| `source_template_example` | `ready` | `True` | `onboarding_example` | `zh-CN` | `internal` | `markdown` | `section` | `ready` | `ready` | 1 | 3 | 3 | 1 | 0 | `in_sync` | `ready` | `bind_source_from_control_plane` |
| `company_profile_2025_trial` | `ready` | `True` | `company_profile` | `zh-CN` | `local_private_trial` | `markdown` | `chunk` | `ready` | `ready` | 1 | 1005 | 1005 | 1 | 0 | `in_sync` | `ready` | `bind_source_from_control_plane` |

## Operation Notes

- This summary is read-only and does not create source-to-agent bindings.
- External control planes own binding policy, approvals, audit, and final answer workflow.
- Detailed document diagnostics remain available from source document manifests and ingestion preflight endpoints.
