# expand-insufficient-evidence-benchmark-cases

## Why

Evidence grading now has local candidate policies, but the current Chinese seed is a happy-path fixture set: both strict citation matching and loose source matching pass every case. That proves the report shape, but it does not yet test the failure modes that matter for runtime answer gating.

The next step is to add a dedicated stress set for evidence grading where retrieval can return related-but-insufficient evidence, miss expected evidence, or return unexpected evidence for an unsupported query. This gives later reranker, answer gate, and query orchestration changes a realistic failure surface without breaking the existing 21-case baseline used by threshold and chunking comparisons.

## What Changes

- Add a dedicated local evidence grading stress fixture.
- Add tests that prove the stress fixture produces `related_insufficient`, `missing_evidence`, and `unexpected_evidence` labels.
- Export checked-in evidence grading stress reports.
- Update README, research notes, architecture docs, and specs to distinguish baseline seed evidence from stress evidence.

## Non-Goals

- Do not change runtime retrieval behavior.
- Do not change `/api/rag/retrieve`.
- Do not replace the existing Chinese seed baseline used by threshold/chunking reports.
- Do not add an LLM grader or reranker.
- Do not modify source documents only to make tests pass.

## Success Criteria

- The stress fixture is separate from `retrieval_benchmark_cases.json`.
- Evidence grading stress reports include at least one `related_insufficient`, one `missing_evidence`, and one `unexpected_evidence` case.
- Existing baseline retrieval tests remain stable.
- Focused and full tests pass.
- The change is archived and main specs validate strictly.
