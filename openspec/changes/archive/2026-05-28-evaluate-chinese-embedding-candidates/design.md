# Design: evaluate-chinese-embedding-candidates

## Approach

Extend the existing local retrieval benchmark module with an embedding candidate evaluation model. This layer is metadata-first: it describes candidate options and produces decision evidence, but does not instantiate real embedding adapters.

The evaluation output is intended for architecture review. Retrieval benchmark metrics still come from the existing benchmark harness, while embedding-specific criteria are recorded as candidate metadata and scored locally against enterprise-readiness fields.

## Candidate Shape

Each candidate includes:

- stable id
- provider family (`hosted`, `local`, or `mock`)
- model name
- deployment mode
- language profile
- vector dimension if known
- data residency posture
- expected operational complexity
- reranker compatibility notes
- status (`baseline`, `candidate`, or `deferred`)

The initial catalog will include:

- `mock-hash-v1`: current deterministic contract baseline.
- `qwen-embedding-candidate`: hosted/public candidate placeholder for Chinese-heavy workloads.
- `bge-m3-local-candidate`: local/private candidate placeholder for Chinese-heavy and multilingual workloads.
- `openai-embedding-candidate`: hosted/public candidate placeholder for cross-language baseline comparison.

These are not approvals. They only make future comparison repeatable.

## Evaluation Output

The report contains:

- candidate metadata
- criteria coverage flags
- readiness status
- decision notes
- optional retrieval benchmark summary if the caller already ran one

Exports remain local JSON / Markdown files under caller-provided paths. This keeps the provider surface small and avoids turning exploratory evaluation into a public API.

## Safety

The implementation must not call external services or load local embedding models. Hosted/local adapter implementations remain fail-closed. Candidate ids are validated before export to avoid unsafe filenames.
