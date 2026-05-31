## Context

`GET /api/provider/source-bindings` already summarizes provider-owned facts that MyPrivateAgent can review before binding a source to an agent. The endpoint is documented and discoverable through the provider manifest endpoints map, but it is not yet represented as a formal capability id. That leaves capability-driven clients unable to request it in preflight or inspect its response schema through the same mechanism used for retrieval, answer, source document manifests, and planned GraphRAG.

## Goals / Non-Goals

**Goals:**

- Make source binding review discoverable from `/api/capabilities`.
- Include the capability id in the manifest and default preflight requirements.
- Keep the capability read-only and evidence-oriented.
- Preserve the external control plane boundary for source-to-agent binding decisions.

**Non-Goals:**

- Create or store source-to-agent bindings.
- Add RBAC, approval, audit, policy, or final answer workflow.
- Execute ingestion jobs, rebuild indexes, run retrieval, call embedding/vector stores, or execute GraphRAG from the capability metadata.
- Change the source binding summary response shape.

## Decisions

- Use capability id `knowledge.provider.source_bindings`.
  - Rationale: The capability belongs to provider integration and binding review rather than document retrieval itself.
  - Alternative considered: `knowledge.rag.source_bindings`; rejected because it could imply the provider owns actual RAG binding policy.

- Represent the invocation as a `GET` capability with a response schema ref and an empty example request.
  - Rationale: Existing preflight accepts GET diagnostic capabilities when they provide a response schema and example request.
  - Alternative considered: No example request; rejected because schema preflight currently treats GET examples as part of discoverability.

- Include the capability in default preflight requirements.
  - Rationale: Source binding readiness is part of the provider's lightweight integration contract for MyPrivateAgent.
  - Alternative considered: Make it optional only; rejected because the endpoint is already implemented and required by handoff evidence.

## Risks / Trade-offs

- Capability id churn could affect early clients that cache capability ids. Mitigation: add it as an additive capability and keep existing ids unchanged.
- External callers may misread the capability as permission to create bindings. Mitigation: descriptions, specs, README, and roadmap explicitly state it is read-only evidence and caller-owned policy remains external.
