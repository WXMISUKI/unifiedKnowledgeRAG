# evaluate-evidence-grading-candidate

## Why

The provider now has benchmark evidence for chunking strategies and deterministic query rewrite candidates. The next mature Agentic RAG pattern to evaluate is evidence grading: separating "retrieved something similar" from "retrieved answer-bearing evidence."

This is especially important for enterprise RAG because high vector scores can still return related-but-insufficient chunks. Before adding a reranker, runtime answer gate, LLM grader, or GraphRAG dependency, the project needs a local evidence shape that can record whether retrieved citations are answer-bearing, insufficient, missing, or intentionally empty.

## What Changes

- Add local evidence grading candidate models and deterministic grading policies.
- Add service-level evaluation helpers that run benchmark retrieval, grade returned evidence, and export JSON/Markdown evidence.
- Preserve retrieval misses and expected-empty outcomes as explicit evidence instead of hiding them behind a pass/fail aggregate.
- Update README, research notes, architecture docs, and main specs with the evidence grading boundary.

## Non-Goals

- Do not add an LLM grader.
- Do not change `/api/rag/retrieve` behavior.
- Do not filter runtime retrieval results.
- Do not approve reranking, hybrid retrieval, or GraphRAG storage.
- Do not change default retrieval backend, chunking strategy, or score threshold.

## Success Criteria

- Evidence grading candidates can be evaluated locally against the current Chinese benchmark seed.
- Exports include candidate metadata, grading metrics, per-case labels, returned citations, expected citations, and decision notes.
- Expected-empty cases remain protected and are reported as "no evidence expected."
- Focused and full tests pass.
- The change is archived and main specs validate strictly.
