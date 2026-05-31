## Context

The roadmap already states that GraphRAG must remain use-case driven and that graph query execution stays planned until relationship-heavy evidence exists. The missing piece is a concrete, local contract that helps reviewers decide whether a candidate question belongs in graph work or should stay in document RAG.

The contract should be a review artifact, not a policy engine. It should make the graph boundary easier to read and keep runtime ownership unchanged.

## Goals / Non-Goals

**Goals:**

- Document the relationship-heavy use cases that are graph-worthy.
- Document the cases that should remain document RAG.
- Keep the contract local, review-oriented, and read-only.

**Non-Goals:**

- Implementing graph execution.
- Adding Neo4j, entity extraction, ontology workflows, or graph query runtime.
- Promoting graph query execution or graph storage by default.

## Decisions

- Treat graph-worthiness as evidence-backed and use-case-driven.
  The contract should name concrete relationship shapes, not a generic "graph is better" claim.

- Keep document RAG as the default for single-document, citation-first, or policy lookup questions.
  Those do not need graph storage or multi-hop reasoning.

- Use explicit source-evidence rules for graph work.
  Graph output should still point back to source documents, import batches, business records, or ontology versions.

## Risks / Trade-offs

- The contract may become stale if the use cases evolve.
  Mitigation: keep the document short, concrete, and linked from the roadmap/tracker.

- Too much graph enthusiasm could blur the boundary.
  Mitigation: list clear non-goals and examples that should stay in document RAG.
