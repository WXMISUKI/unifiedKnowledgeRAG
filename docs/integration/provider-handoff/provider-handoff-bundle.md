# Provider Handoff Bundle

- Report: `provider-handoff-bundle-v1`
- Status: `review`
- Generated At: `2026-05-30T07:32:00.460469+00:00`
- Provider: `unifiedKnowledgeProvider`
- Contract: `knowledge-provider-contract-v1`
- Manifest: `provider-integration-manifest-v1`

## Evidence Artifacts

| Artifact | Category | Present | Status | Summary | Recommended Action |
|---|---|---|---|---|---|
| `provider_integration_probe` | `integration` | `True` | `ready` | bindable=True; checks=6; capabilities=4 | `no_action_required` |
| `provider_contract_smoke` | `contract` | `True` | `ready` | passed=True; checks=8/8 | `no_action_required` |
| `deployment_readiness` | `operations` | `True` | `review` | status=review | `review_evidence_notes` |
| `reindex_readiness` | `operations` | `True` | `ready` | status=ready | `no_action_required` |

## Operation Notes

- This bundle is a read-only handoff index over existing local evidence files.
- Regenerate prerequisite evidence reports after configuration, dependency, source, or index lifecycle changes.
- External control planes still own provider registration, heartbeat governance, audit policy, and source-to-agent binding decisions.
- At least one evidence artifact requires human review before promotion.
