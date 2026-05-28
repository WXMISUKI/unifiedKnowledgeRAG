# Design: Retrieval Candidate Evaluation

## Overview

Candidate evaluation builds on the existing benchmark report model. A candidate is a named configuration plus metadata. The runner executes the existing benchmark harness once per candidate and can export each result as JSON and Markdown.

## Data Model

`RetrievalCandidate` contains:

- `id`: stable lowercase identifier used in output filenames
- `backend`: retrieval backend name, matching current `Settings.rag_retrieval_backend`
- `description`: human-readable summary
- `metadata`: optional local evidence metadata, such as `embedding`, `vector_store`, `reranker`, or `notes`

`RetrievalCandidateEvaluation` contains:

- `candidate`: candidate definition
- `report`: benchmark report for that candidate
- `json_path`: optional exported JSON path
- `markdown_path`: optional exported Markdown path

## Execution

The runner accepts benchmark cases and candidate definitions. For each candidate it creates a `Settings` object scoped to that candidate backend and calls `run_retrieval_benchmark`.

This first slice deliberately only maps candidates to existing local backends. It does not add a production embedding/vector-store adapter. Future changes can extend candidate settings after we agree on concrete providers.

## Export

When an output directory is provided, each candidate writes:

- `<candidate-id>.json`
- `<candidate-id>.md`

The exported files use the existing benchmark report export helpers so the evidence format stays consistent.

## Guardrails

- Candidate IDs must be unique within a run.
- Candidate IDs must be filesystem-friendly.
- Candidate evaluation remains service-only and local.
- No production infrastructure dependency is introduced by this change.
