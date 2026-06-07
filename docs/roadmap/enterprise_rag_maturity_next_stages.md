# Enterprise RAG Maturity Next Stages

## Purpose

This note keeps the next RAG work practical. The goal is to make the local provider useful for real business knowledge-base trials before adding heavier retrieval infrastructure.

## Direction

| Stage | Primary Goal | Repository Focus | Completion Signal | Non-Goals |
| --- | --- | --- | --- | --- |
| 1. MyPrivateAgent business Q&A loop | A caller can ask a real business question and receive a grounded, citation-limited answer preview | `MyPrivateAgent` | Provider corpus trial and explicit grounded-answer API both return `go`; one closure report says whether local business use can proceed | No default `/api/chat` injection, no GraphRAG, no source binding mutation |
| 2. Provider document ingestion loop | A business document can become managed RAG material through a clear local ingestion path | `unifiedKnowledgeRAG` | Source registration, chunk manifest, index readiness, and retrieval smoke are visible for one approved document | No full OCR platform, no multi-tenant governance, no runtime backend promotion |
| 3. Parser adapter boundary | PDF/Word/Excel/OCR outputs can enter the ingestion loop through normalized text/artifact contracts | Both repos as needed | External parser outputs can be converted into provider-managed source artifacts with traceable provenance | No embedding parser engines deeply inside the provider by default |
| 4. Vector backend candidate review | Qdrant/pgvector and embedding candidates can be evaluated against real corpus cases | `unifiedKnowledgeRAG` | Quality, latency, filtering, reindex, and rollback evidence are enough for review | No default vector-store switch from a single smoke result |
| 5. Retrieval quality maturity | Chunking, metadata filters, hybrid search, rerank, and negative controls are judged by repeatable cases | `unifiedKnowledgeRAG` | Customer-like benchmark shows improved answerability without cross-domain false positives | No local micro-optimization without business cases |
| 6. GraphRAG use-case gate | Graph execution starts only when relationship-heavy questions justify it | `unifiedKnowledgeRAG` | A concrete graph-worthy use case, schema, source evidence rules, and benchmark are approved | No Neo4j, ontology workflow, or graph query execution by default |

## Immediate Next Stage

Stage 1 in `MyPrivateAgent` is closed for the current local company profile trial. Stage 2 in `unifiedKnowledgeRAG` is closed for the local approved-source ingestion loop. Stage 3 boundary definition and Stage 3b parser-artifact-to-local-ingestion loop are closed. The immediate next slice is the parser-derived corpus retrieval quality baseline before any Stage 4 candidate backend review.

The quality baseline command should verify answerable parser-derived business questions, expected-empty negative controls, citation match rate, and invalid citation count while keeping Qdrant/pgvector/BGE-M3 promotion, parser/OCR execution, MyPrivateAgent orchestration, source binding, and GraphRAG execution out of provider defaults.

## Stage 2 Local Ingestion Loop

The local operator entrypoint is:

`python scripts/export_local_approved_source_ingestion_loop.py`

It writes:

- `docs/local-run/approved-source-ingestion-loop/local-approved-source-ingestion-loop.json`
- `docs/local-run/approved-source-ingestion-loop/local-approved-source-ingestion-loop.md`

This loop creates only an explicit local ingestion job for the selected source. It does not parse raw PDFs, start OCR services, call MyPrivateAgent, create source-to-agent bindings, mutate `/api/chat`, promote retrieval defaults, introduce background workers, or execute GraphRAG.

## Stage 3 Parser Artifact Boundary

The local operator entrypoint is:

`python scripts/export_normalized_parser_artifact_ingestion_boundary.py`

It writes:

- `docs/local-run/normalized-parser-artifact-boundary/normalized-parser-artifact-boundary.json`
- `docs/local-run/normalized-parser-artifact-boundary/normalized-parser-artifact-boundary.md`
- `docs/local-run/normalized-parser-artifact-boundary/parser-derived-source.md`
- `docs/local-run/normalized-parser-artifact-boundary/parser-derived-source-overlay.json`

This loop accepts only a normalized external parser artifact JSON file. It does not parse raw PDFs, start OCR services, call parser engines, create ingestion jobs, promote retrieval defaults, create source-to-agent bindings, call MyPrivateAgent, or execute GraphRAG.

## Stage 3b Parser Artifact Local Ingestion Loop

The local operator entrypoint is:

`python scripts/export_parser_artifact_local_ingestion_loop.py`

It writes:

- `docs/local-run/parser-artifact-local-ingestion-loop/parser-artifact-local-ingestion-loop.json`
- `docs/local-run/parser-artifact-local-ingestion-loop/parser-artifact-local-ingestion-loop.md`

This loop orchestrates the normalized parser artifact boundary and the existing approved-source ingestion loop. It does not parse raw PDFs, start OCR services, call parser engines, create source-to-agent bindings, call MyPrivateAgent, promote retrieval defaults, or execute GraphRAG.

## Parser-Derived Corpus Retrieval Quality Baseline

The local operator entrypoint is:

`python scripts/export_parser_derived_corpus_retrieval_quality_baseline.py`

It writes:

- `docs/local-run/parser-derived-corpus-retrieval-quality-baseline/parser-derived-corpus-retrieval-quality-baseline.json`
- `docs/local-run/parser-derived-corpus-retrieval-quality-baseline/parser-derived-corpus-retrieval-quality-baseline.md`

This baseline evaluates a small parser-derived company-profile query set with answerable and expected-empty cases. It does not promote Qdrant, pgvector, BGE-M3, hybrid search, rerankers, chunking defaults, MyPrivateAgent orchestration, or GraphRAG execution.
