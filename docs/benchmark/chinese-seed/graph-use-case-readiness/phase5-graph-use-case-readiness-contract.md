# Phase 5 Graph Use-Case Readiness Contract

- Report: `phase5-graph-use-case-readiness-contract-v1`
- Status: `review`
- Scope: `GraphRAG readiness`
- Generated At: `2026-05-31`

## Purpose

This contract explains when a question is a graph-worthy use case and when it should remain in document RAG.
It is intentionally read-only and review-oriented. The provider remains a boundary, not the owner of graph execution policy.

## Graph-Worthy Cases

Use GraphRAG readiness work when the question is relationship-heavy and needs more than a document citation:

- multi-entity relationship tracing
- path and multi-hop reasoning
- order, logistics, and refund relationships
- customer-product-contract-risk relationships
- person-location-case-event relationships

These cases justify graph readiness work only when the evidence needs entity, relation, or path traversal rather than a single source document.

## Document-RAG-Only Cases

Keep the question in document RAG when it is primarily:

- a policy lookup from one source family
- a citation-first FAQ answer
- a keyword, identifier, or section lookup
- a single-document explanation with no meaningful relation chain

If a question can be answered by stable citations from document retrieval, graph storage is not required.

## Graph Evidence Rules

Graph output, when eventually implemented, should remain provider-neutral and serializable.
The evidence should point back to the underlying source of truth:

- source documents
- import batches
- business system records
- ontology versions

The provider must not expose internal graph objects, database cursors, or execution internals as the public contract.

## Non-Goals

- Graph query execution
- Neo4j dependency promotion
- Entity extraction pipeline implementation
- Ontology workflow implementation
- Source-to-graph indexing
- Default GraphRAG runtime promotion

## Current Evidence

- `docs/roadmap/lightweight_provider_roadmap.md`
- `docs/integration/provider-binding/provider-integration-probe.md`
- `docs/smoke/provider-contract/provider-contract-smoke.md`
- `docs/operations/deployment-readiness/deployment-readiness.md`

## Notes

- GraphRAG should stay optional until the use case is concrete and the ownership of graph operations is explicit.
- The contract does not make graph query execution ready; it only explains the readiness boundary.
