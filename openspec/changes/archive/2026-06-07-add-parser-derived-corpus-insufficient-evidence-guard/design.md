# Design: Parser-Derived Corpus Insufficient Evidence Guard

## Scope

This change targets parser-derived local corpus retrieval quality for the current company-profile trial source. The goal is to prevent broad lexical fallback from treating unrelated missing-field questions as answerable.

## Approach

Add a small query evidence guard in the RAG retrieval path after candidate documents are retrieved and before they are returned or passed to the deterministic answer composer.

The guard is intentionally conservative:

- It applies only to source-scoped local retrieval requests where returned documents all come from parser-derived/local document sources.
- It uses query intent cues for known enterprise missing-field categories such as contract amounts, staff rosters, compensation, phone numbers, and other field-like facts.
- If the query asks for a field-like fact and the returned snippets do not contain supporting lexical cues for that field, the provider returns an empty document list.
- Empty documents already cause `evidence_pack.status=insufficient_evidence` and deterministic answer status `insufficient_evidence`.

## Why Not Tune Thresholds Only

The current mock/local retrieval backend can return broad related chunks with high-enough scores because the query and source share company/profile terms. Raising global thresholds would risk breaking positive business-scope questions. A narrow missing-field guard is safer for this local stage.

## Boundaries

- The guard does not promote a candidate backend.
- The guard does not introduce LLM answer composition.
- The guard does not create source bindings.
- The guard does not execute GraphRAG.
- The guard can later be replaced or narrowed by better metadata filters, hybrid search, rerankers, or field-aware extraction once real corpus demand justifies them.
