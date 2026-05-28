# Change: export-chinese-seed-evaluation-evidence

## Summary

Add a local helper that exports the current Chinese benchmark seed evidence for retrieval and embedding candidate review.

## Motivation

The project now has a larger Chinese benchmark seed and metadata-only embedding candidate evaluation. The next step is to make evidence generation repeatable so future OpenSpec changes can reference stable JSON and Markdown report files instead of relying on ad hoc Python snippets.

This keeps the workflow local and review-oriented. It does not approve a production embedding model, call hosted services, or promote Qdrant.

## Goals

- Provide a service-level helper to export the default Chinese seed evidence bundle.
- Export fixture retrieval baseline evidence from the current benchmark cases.
- Export embedding candidate metadata reports for the current candidate catalog.
- Document the local report paths and clarify that seed evidence is not production acceptance.

## Non-Goals

- Do not add public HTTP APIs or CLI commands.
- Do not run live Qdrant as part of the default evidence bundle.
- Do not call hosted/local embedding providers.
- Do not select a production embedding, reranker, vector database, or GraphRAG store.
