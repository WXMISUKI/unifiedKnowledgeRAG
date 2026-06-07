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

Start with Stage 1 in `MyPrivateAgent`: close the local business Q&A user loop over the current `company_profile_2025_trial` corpus.

This keeps the current provider work from drifting into more evidence documents. If Stage 1 is `go`, the next provider-side stage should be document ingestion rather than GraphRAG.

