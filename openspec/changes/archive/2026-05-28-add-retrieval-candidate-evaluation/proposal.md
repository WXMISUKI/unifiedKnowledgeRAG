# Proposal: Add Retrieval Candidate Evaluation

## Summary

Add a local, provider-neutral evaluation layer that runs the same retrieval benchmark cases against named candidate configurations and exports comparable evidence reports.

## Motivation

The project now has a benchmark harness and report export helpers, but candidate comparison is still ad hoc: callers must manually construct settings, run reports one by one, and decide how evidence should be grouped.

Before choosing a production embedding model, vector database, reranker, or hybrid retrieval path, we need a repeatable local workflow that:

- names each candidate explicitly
- records candidate metadata without adding production dependencies
- runs each candidate through the same benchmark cases
- exports per-candidate JSON and Markdown evidence files

This keeps future infrastructure decisions evidence-led while preserving the current provider-neutral boundary.

## Scope

In scope:

- local candidate definition data model
- local candidate evaluation runner
- stable output naming for per-candidate evidence reports
- tests for candidate metadata, multi-candidate execution, and export paths
- README and architecture-document guidance

Out of scope:

- selecting a production embedding model
- selecting or adding a vector database
- adding reranker, hybrid retrieval, or external queue dependencies
- exposing candidate evaluation over HTTP
- introducing a CLI wrapper

## Impact

This change extends `app.services.retrieval_benchmark` as a local service-only utility. It should not affect existing provider HTTP contracts or runtime retrieval behavior.
