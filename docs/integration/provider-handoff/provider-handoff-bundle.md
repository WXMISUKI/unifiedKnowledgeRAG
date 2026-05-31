# Provider Handoff Bundle

- Report: `provider-handoff-bundle-v1`
- Status: `review`
- Generated At: `2026-05-31T07:52:28.898066+00:00`
- Provider: `unifiedKnowledgeProvider`
- Contract: `knowledge-provider-contract-v1`
- Manifest: `provider-integration-manifest-v1`

## Evidence Artifacts

| Artifact | Category | Present | Status | Summary | Recommended Action |
|---|---|---|---|---|---|
| `provider_integration_probe` | `integration` | `True` | `ready` | bindable=True; checks=6; capabilities=5 | `no_action_required` |
| `provider_contract_smoke` | `contract` | `True` | `ready` | passed=True; checks=9/9 | `no_action_required` |
| `deployment_readiness` | `operations` | `True` | `review` | status=review | `review_evidence_notes` |
| `reindex_readiness` | `operations` | `True` | `ready` | status=ready | `no_action_required` |
| `source_binding_summary` | `source-binding` | `True` | `ready` | status=ready; bindable_sources=2/2; source_statuses=ready:2; recommended_actions=bind_source_from_control_plane:2 | `no_action_required` |
| `deployed_provider_smoke` | `deployed-integration` | `False` | `review` | Optional deployed evidence is missing. | `run_deployed_provider_smoke_after_deployment` |
| `phase3_seed_retrieval_baseline` | `retrieval-evidence` | `True` | `ready` | total_cases=26; hit_rate=0.9615; citation_match_rate=0.9615; empty_handling_rate=0.9000 | `no_action_required` |
| `phase3_fp_fn_review` | `retrieval-evidence` | `True` | `ready` | false_positive_count=1; false_negative_count=0; false_positive_rate=0.0385; false_negative_rate=0.0000 | `no_action_required` |

## Operation Notes

- This bundle is a read-only handoff index over existing local evidence files.
- Regenerate prerequisite evidence reports after configuration, dependency, source, or index lifecycle changes.
- External control planes still own provider registration, heartbeat governance, audit policy, and source-to-agent binding decisions.
- At least one evidence artifact requires human review before promotion.
- Deployed provider smoke evidence is optional before deployment; run it against the deployed base URL before external binding.
