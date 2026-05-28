# Chunking Strategy Candidate Evaluation

| Candidate | Status | Total Chunks | Citation Stability | Long-Section Support |
| --- | --- | ---: | --- | --- |
| markdown-paragraph-v1 | implemented | 11 | stable | covered |
| markdown-section-v1 | planned |  | planned | planned |
| token-window-v1 | planned |  | planned | planned |

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
- Decision note: Candidate is not runnable yet; no retrieval metrics are claimed.
- Decision note: Implement runnable benchmark evidence before production promotion.

### token-window-v1

- Description: Planned token-window chunking with overlap for long dense content.
- Expected fit: long paragraphs, pasted policy text, PDF/Word extracted body text
- Source ids: refund_policy_docs, logistics_faq
- Trade-off: May improve recall inside long dense sections.
- Trade-off: Can duplicate evidence and complicate citation stability.
- Trade-off: Requires tokenizer-aware sizing and overlap decisions.
- Decision note: Candidate is not runnable yet; no retrieval metrics are claimed.
- Decision note: Implement runnable benchmark evidence before production promotion.
