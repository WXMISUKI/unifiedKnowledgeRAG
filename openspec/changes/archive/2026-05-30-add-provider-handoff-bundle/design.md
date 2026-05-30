## Context

`unifiedKnowledgeRAG` is intended to be consumed as a lightweight external knowledge provider. Recent changes produced multiple review artifacts:

- `docs/integration/provider-binding/provider-integration-probe.json`
- `docs/smoke/provider-contract/provider-contract-smoke.json`
- `docs/operations/deployment-readiness/deployment-readiness.json`
- `docs/operations/reindex-readiness/reindex-readiness.json`

These files are valuable, but external callers benefit from a single handoff index that answers: "Can I bind this provider, what evidence exists, what is missing, and what should I review next?"

## Approach

1. Add a service-level handoff bundle builder.
   - Read existing JSON evidence files when present.
   - Include provider identity from `build_provider_manifest()`.
   - Include summary rows for required evidence artifacts.
   - Compute a conservative bundle status:
     - `blocked` if a required artifact is missing or clearly failed.
     - `review` if an artifact asks for review or is degraded.
     - `ready` if required artifacts are present and their primary statuses are acceptable.
2. Add JSON and Markdown render/export helpers.
3. Add a CLI script to export the bundle.
4. Add focused tests for present, missing, failed, and review-state evidence.

## Report Shape

The bundle will be versioned as `provider-handoff-bundle-v1` and include:

- provider identity and contract version
- generated timestamp
- overall status
- evidence artifact rows:
  - id
  - category
  - path
  - present
  - status
  - summary
  - recommended action
- operation notes

## Read-Only Boundary

The handoff bundle only reads existing local files and provider manifest metadata. It must not regenerate prerequisite reports, call FastAPI endpoints, execute retrieval or answer logic, create ingestion jobs, rebuild indexes, download models, call Qdrant, or execute GraphRAG.

## Risks

- Evidence can be stale if prerequisite reports are not regenerated. Mitigation: include file path and status, and document the prerequisite export commands.
- Status schemas differ between reports. Mitigation: keep extraction small and explicit per known artifact id, and default unknown/missing status to review or blocked rather than pretending readiness.
