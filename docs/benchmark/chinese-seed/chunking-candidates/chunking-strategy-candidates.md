# Chunking Strategy Candidate Evaluation

| Candidate | Status | Total Chunks | Citation Stability | Long-Section Support |
| --- | --- | ---: | --- | --- |
| markdown-paragraph-v1 | implemented | 11 | stable | covered |
| markdown-section-v1 | runnable | 2 | stable | covered-by-section |
| token-window-v1 | runnable | 8 | stable | covered-by-window |

## Candidate Notes

### markdown-paragraph-v1

- Description: Current local markdown paragraph baseline used by Qdrant ingestion.
- Expected fit: simple markdown, short procedures, deterministic local evidence
- Source ids: refund_policy_docs, logistics_faq
- Trade-off: Stable and easy to audit.
- Trade-off: Can be too coarse when one paragraph contains several details.
- Trade-off: Does not model PDF/Word structure or token overlap.
- Decision note: This is the current runtime Qdrant markdown ingestion baseline.
- Decision note: Use retrieval benchmark evidence before deciding whether to replace it.

### markdown-section-v1

- Description: Planned section-aware markdown chunking using headings and paragraphs.
- Expected fit: manuals, policy sections, documents with useful headings
- Source ids: refund_policy_docs, logistics_faq
- Trade-off: May improve citation context for long sections.
- Trade-off: Needs heading-aware citation and section boundary rules.
- Trade-off: Still does not solve scanned documents or tables.
- Decision note: Candidate can generate section chunks for local markdown sources.
- Decision note: Runtime Qdrant ingestion still uses markdown-paragraph-v1.
- Decision note: Retrieval metrics are not claimed until a future runnable retrieval benchmark is added.

### token-window-v1

- Description: Runnable token-window chunking with overlap for long dense content.
- Expected fit: long paragraphs, pasted policy text, PDF/Word extracted body text
- Source ids: refund_policy_docs, logistics_faq
- Trade-off: May improve recall inside long dense sections.
- Trade-off: Can duplicate evidence and complicate citation stability.
- Trade-off: Uses a deterministic lightweight tokenizer until production tokenizer evidence exists.
- Decision note: Candidate can generate overlapping token-window chunks for local markdown sources.
- Decision note: Runtime Qdrant ingestion still uses markdown-paragraph-v1.
- Decision note: Use Qdrant+BGE smoke comparison before promoting this strategy.
