# Proposal: Parser-Derived Corpus Insufficient Evidence Guard

## Why

The current parser-derived company-profile quality baseline answers positive business questions correctly, but expected-empty negative controls still retrieve generic company-profile chunks. That means the local business RAG path can return plausible-looking evidence for facts that are not present in the document.

For a practical enterprise knowledge base, the provider must know when to say `insufficient_evidence`. This change closes that gap for parser-derived local corpus trials without promoting vector stores, hybrid search, rerankers, answer composer ownership, or GraphRAG.

## What Changes

- Add a lightweight insufficient-evidence guard for parser-derived local corpus retrieval.
- Preserve positive retrieval behavior for answerable company-profile questions.
- Ensure expected-empty company-profile negative controls return no retrieved evidence and no answer citations.
- Refresh the parser-derived corpus retrieval quality baseline after implementation.

## Non-Goals

- Do not enable GraphRAG.
- Do not switch runtime defaults to Qdrant, pgvector, BGE-M3, hybrid search, or rerankers.
- Do not build a general evaluation platform.
- Do not move final user-facing answer policy into the provider.
- Do not change MyPrivateAgent `/api/chat` behavior or source binding state.
