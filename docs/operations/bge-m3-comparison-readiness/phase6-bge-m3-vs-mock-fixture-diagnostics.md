# Phase 6 BGE-M3 vs Mock/Fixture Diagnostics

- Report: `phase6-bge-m3-vs-mock-fixture-diagnostics-v1`
- Status: `review`
- Decision: `keep_runtime_defaults`
- Generated At: `2026-06-04T09:31:25.426494+00:00`

## Summary

| Metric | Value |
|---|---|
| Total Signals | `7` |
| Ready Signals | `5` |
| Review Signals | `2` |
| Blocked Signals | `0` |
| Open Signal IDs | `["artifact_readiness_linkage", "quality_non_regression_visibility"]` |

## Baseline vs Candidate

| Field | Baseline | Candidate | Delta |
|---|---|---|---|
| Hit Rate | `0.9062` | `0.7619` | `-0.1443` |
| Citation Match Rate | `0.9062` | `0.7619` | `-0.1443` |
| Empty Handling Rate | `0.7500` | `0.2857` | `-0.4643` |
| Average Latency (ms) | `0.2368` | `324.7621` | `324.5253` |

## Linkage

| Field | Value |
|---|---|
| Artifact Readiness Present | `True` |
| Artifact Readiness Status | `review` |
| Deployment Readiness Present | `True` |
| Deployment Readiness Status | `review` |
| Runtime Diagnostics Present | `True` |
| Runtime Diagnostics Status | `review` |
| Latency Diagnostics Present | `True` |
| Latency Diagnostics Status | `review` |

## Signals

| Signal | Status | Summary | Recommended Action |
|---|---|---|---|
| `baseline_profile_presence` | `ready` | present=True; total_cases=32 | `no_action_required` |
| `candidate_profile_presence` | `ready` | present=True; total_cases=21 | `no_action_required` |
| `comparison_metric_schema` | `ready` | baseline_core_metrics=True; candidate_core_metrics=True | `no_action_required` |
| `artifact_readiness_linkage` | `review` | artifact_present=True; artifact_status=review | `review_bge_m3_artifact_readiness` |
| `runtime_and_latency_diagnostics_linkage` | `ready` | runtime_status=review; latency_status=review | `no_action_required` |
| `quality_non_regression_visibility` | `review` | hit_rate_delta=-0.1443; citation_match_rate_delta=-0.1443; empty_handling_rate_delta=-0.4643 | `expand_candidate_cases_and_review_fp_fn` |
| `deployment_linkage_visibility` | `ready` | deployment_present=True; deployment_status=review | `no_action_required` |

## Notes

- This report is local read-only comparison evidence and does not change runtime defaults.
- Candidate deltas are interpreted as review guidance, not direct promotion approval.
- Use matching benchmark fixture scope when comparing baseline and candidate evidence.
