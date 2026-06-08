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

Stage 1 in `MyPrivateAgent` is closed for the current local company profile trial. Stage 2 in `unifiedKnowledgeRAG` is closed for the local approved-source ingestion loop. Stage 3 boundary definition, Stage 3b parser-artifact-to-local-ingestion loop, and the local PDF parser provider bridge are closed for the current local company-profile trial. The current practical state is: a real local PDF can be parsed by an operator-started PaddleOCR service, normalized into a parser artifact, and ingested through the existing local RAG loop with `decision=go`.

The current MyPrivateAgent real business trial also returns `go` for the company-profile PDF: answerable business questions produce cited answers, and the negative-control refund-policy question returns `insufficient_evidence` without citations. This closes the current local usability loop.

The next provider-side maturity slice has converted the current real trial into reusable quality measurement:

`Local Business RAG Golden Cases And Chunk Quality Baseline`

Reference decision note:

`docs/roadmap/rag_techniques_experience_application.md`

This stage applies lessons from `RAG_Techniques`: mature RAG changes should be selected by failure mode, not by popularity. The provider now has a local business RAG golden-case report for `company_profile_2025_trial` with `decision=go`, `hit_rate=1.0`, `citation_match_rate=1.0`, `empty_handling_rate=1.0`, and chunk-quality diagnostics over 1005 chunks. The tiny chunk ratio is `0.41`, so the current trial is usable, but future answer-quality regressions should review chunk merging or contextual headers before adopting heavier retrieval techniques.

Qdrant/pgvector/BGE-M3 promotion, parser/OCR service ownership, source binding, and GraphRAG execution remain outside provider defaults.

## RAG_Techniques Experience Adoption

The project should adopt these lessons now:

- Treat RAG as an evaluable pipeline, not a single retriever.
- Maintain golden questions with answerable and insufficient-evidence cases.
- Measure chunk quality before changing chunking defaults.
- Classify failures into parser/OCR, chunking, query mismatch, retrieval quality, citation/evidence, provider availability, or caller/operator flow.
- Preserve citation allowlists and insufficient-evidence fail-closed behavior as hard gates.

The project should adopt these only when triggered by real failures:

- Query rewrite, step-back, sub-query, HyDE, or HyPE when user wording repeatedly misses document evidence.
- Rerank when recall is sufficient but top-k precision is noisy.
- Hybrid/fusion retrieval when keyword and semantic retrieval each solve different accepted cases.
- RAPTOR when long-document hierarchy failures are observed.
- Self-RAG/CRAG when retrieval sufficiency correction is needed with strict loop limits.
- GraphRAG only for relationship-heavy, entity/path/multi-hop questions.

The project should not adopt notebook code, GraphRAG, rerank, hybrid retrieval, or vector backend promotion by popularity alone.

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

## Local PDF Parser Provider Bridge

The local operator entrypoint is:

`python scripts/export_local_pdf_parser_provider_bridge.py --pdf-path "<local-pdf>" --provider-url http://127.0.0.1:8080 --provider-path /ocr --max-pages 5`

It writes:

- `docs/local-run/local-pdf-parser-provider-bridge/local-pdf-parser-provider-bridge.json`
- `docs/local-run/local-pdf-parser-provider-bridge/local-pdf-parser-provider-bridge.md`
- `docs/local-run/local-pdf-parser-provider-bridge/parser-artifacts/local-pdf-parser-artifact.json`

This bridge calls an already-running PaddleOCR-compatible HTTP provider, writes a normalized parser artifact, and reuses the existing parser-artifact local ingestion loop. It does not start PaddleOCR, call MyPrivateAgent, create source-to-agent bindings, mutate `/api/chat`, promote retrieval defaults, introduce background workers, or execute GraphRAG.

## Parser-Derived Corpus Retrieval Quality Baseline

The local operator entrypoint is:

`python scripts/export_parser_derived_corpus_retrieval_quality_baseline.py`

It writes:

- `docs/local-run/parser-derived-corpus-retrieval-quality-baseline/parser-derived-corpus-retrieval-quality-baseline.json`
- `docs/local-run/parser-derived-corpus-retrieval-quality-baseline/parser-derived-corpus-retrieval-quality-baseline.md`

This baseline evaluates a small parser-derived company-profile query set with answerable and expected-empty cases. The current company-profile baseline is `go`: answerable cases keep source/citation coverage, and expected-empty contract-amount/staff-roster questions now return `insufficient_evidence` without endorsed citations. It does not promote Qdrant, pgvector, BGE-M3, hybrid search, rerankers, chunking defaults, MyPrivateAgent orchestration, or GraphRAG execution.

## Local Business RAG Golden Cases And Chunk Quality Baseline

The local operator entrypoint is:

`python scripts/export_local_business_rag_golden_cases.py`

It writes:

- `docs/local-run/business-rag-golden-cases/company-profile-golden-cases.json`
- `docs/local-run/business-rag-golden-cases/local-business-rag-golden-cases.json`
- `docs/local-run/business-rag-golden-cases/local-business-rag-golden-cases.md`

The current report is `go`: 4 answerable business cases and 2 expected-empty negative controls pass with citation allowlists intact. Chunk-quality diagnostics show `total_chunk_count=1005`, `tiny_chunk_ratio=0.41`, `citation_coverage_ratio=1.0`, and `page_coverage_count=10`. This is evidence for repeatable quality review, not a chunking-default promotion. Future real-document failures should be classified against this baseline before considering query rewrite, rerank, hybrid retrieval, RAPTOR, Self/Corrective RAG, or GraphRAG.

## Real Business Corpus Golden Case Expansion

The aggregate local operator entrypoint is:

`python scripts/export_real_business_corpus_golden_cases.py`

It writes:

- `docs/local-run/business-rag-golden-cases/real-business-corpus-golden-cases.json`
- `docs/local-run/business-rag-golden-cases/real-business-corpus-golden-cases.md`

The current aggregate report is `go` with `source_count=1`, `case_count=6`, `hit_rate=1.0`, `citation_match_rate=1.0`, and `empty_handling_rate=1.0`. This stage intentionally keeps the aggregate fixture compatible with the existing company-profile baseline while adding `source_id`, `failure_mode`, and `risk_level` fields so future real documents or real failed questions can be appended without changing code.

Because the aggregate evidence still has no accepted failure, the next provider action is to add more real business documents or real failed questions. Advanced RAG strategy changes remain untriggered until the aggregate report shows a concrete failure mode such as chunking, query mismatch, retrieval quality, citation/evidence, parser/OCR, caller/operator flow, or graph use-case demand.
