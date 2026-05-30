## Overview

The roadmap should answer three questions:

1. What is this module responsible for?
2. What phase are we in?
3. What evidence must exist before we promote a capability or dependency?

The design intentionally avoids turning the provider into a full agent runtime. The provider may expose retrieval, cited answer context, graph boundaries, health, manifest, preflight, and evidence reports. It should not own agent identity, policy, approval, final response style, conversation memory, or task execution.

## Phase Model

Use short, evidence-driven phases:

- Phase 0: Provider contract and binding baseline.
- Phase 1: Lightweight roadmap and phase gates.
- Phase 2: Enterprise document ingestion and chunking baseline.
- Phase 3: Retrieval quality promotion gates.
- Phase 4: Evidence packaging for caller-owned answer generation.
- Phase 5: GraphRAG only after a concrete relationship-heavy use case.
- Phase 6: Operational readiness for external provider deployment.

## Gate Principles

- Every future OpenSpec change should name its target phase.
- Runtime defaults should change only after evidence exists.
- Candidate evaluation is allowed before production approval, but it must remain explicit and reversible.
- GraphRAG, reranker, hybrid retrieval, LLM answer composition, and production queues remain separate approval gates.
- The provider should return trustworthy evidence and metadata; callers decide final answer policy and presentation.

## Non-Goals

- No new code behavior in this change.
- No new database, queue, LLM, graph store, reranker, or agent framework dependency.
- No movement of MyPrivateAgent responsibilities into this provider.
- No claim that existing candidate evidence is production approval.
