# Design: expand-chinese-retrieval-benchmark-cases

## Approach

Extend the existing local fixture assets in place:

- Add more paragraphs to the markdown source documents.
- Mirror those paragraphs as fixture `DocumentChunk` entries with stable citations.
- Add benchmark cases that target the new evidence.
- Update tests to assert category coverage, case count, and deterministic fixture metrics.

This keeps the benchmark harness cheap and repeatable while giving later embedding candidate evaluation a better seed signal.

## Case Design

The added cases should include:

- Chinese paraphrases that do not exactly repeat source text.
- Operational escalation questions.
- SLA/timeliness questions.
- Exception and non-refundable policy questions.
- Cross-source questions that require choosing the best source from multiple knowledge bases.
- Empty questions with business-like but unsupported topics.

## Safety

The fixture backend remains deterministic keyword/bigram scoring. The benchmark should not claim semantic quality from fixture results; it only proves expected evidence contracts and gives real backends a stable comparison set later.
