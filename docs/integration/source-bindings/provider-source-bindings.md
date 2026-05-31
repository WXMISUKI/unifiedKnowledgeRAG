# Provider Source Binding Summary

- Report: `provider-source-binding-summary-v1`
- Status: `ready`
- Generated At: `2026-05-31T02:12:10.079493+00:00`
- Provider: `unifiedKnowledgeProvider`
- Contract: `knowledge-provider-contract-v1`

## Sources

| Source | Status | Bindable | Backend | Index | Drift | Preflight | Recommended Action |
|---|---|---|---|---|---|---|---|
| `refund_policy_docs` | `ready` | `True` | `ready` | `ready` | `in_sync` | `ready` | `bind_source_from_control_plane` |
| `logistics_faq` | `ready` | `True` | `ready` | `ready` | `in_sync` | `ready` | `bind_source_from_control_plane` |

## Operation Notes

- This summary is read-only and does not create source-to-agent bindings.
- External control planes own binding policy, approvals, audit, and final answer workflow.
- Detailed document diagnostics remain available from source document manifests and ingestion preflight endpoints.
