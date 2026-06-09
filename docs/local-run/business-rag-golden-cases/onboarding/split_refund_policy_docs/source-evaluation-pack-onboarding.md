# Source Evaluation Pack Onboarding

- Report: `source-evaluation-pack-onboarding-v1`
- Generated At: `2026-06-09T04:16:09.773719+00:00`
- Source ID: `split_refund_policy_docs`
- Output Dir: `docs\local-run\business-rag-golden-cases\onboarding\split_refund_policy_docs`

## Summary

| Metric | Value |
|---|---|
| `template_count` | `3` |
| `pack_types` | `["baseline_pack", "failed_question_pack", "confirmation_pack"]` |
| `output_dir` | `docs\local-run\business-rag-golden-cases\onboarding\split_refund_policy_docs` |

## Generated Templates

| Pack Type | Path | Template Cases | Notes |
|---|---|---:|---|
| `baseline_pack` | `docs\local-run\business-rag-golden-cases\onboarding\split_refund_policy_docs\baseline-pack.fixture.template.json` | `2` | `Start with answerable and insufficient-evidence golden cases for the new source.` |
| `failed_question_pack` | `docs\local-run\business-rag-golden-cases\onboarding\split_refund_policy_docs\failed-question-pack.fixture.template.json` | `1` | `Use for difficult, failed, or boundary questions after baseline exists.` |
| `confirmation_pack` | `docs\local-run\business-rag-golden-cases\onboarding\split_refund_policy_docs\confirmation-pack.fixture.template.json` | `2` | `Use only when a repeated failure candidate needs a narrower confirmation verdict.` |

## Recommended Next Steps

- fill_baseline_template_with_real_answerable_and_insufficient_evidence_cases
- export_real_pack_only_after_template_fields_are_replaced_with_real_questions
- use_failed_question_pack_after_a_source_has_a_passing_or_reviewable_baseline
- use_confirmation_pack_only_for_repeated_failure_candidates
- update_source_evaluation_pack_catalog_after_real_pack_artifacts_exist

## Non-Goals

- does_not_run_retrieve_or_answer_evaluation
- does_not_generate_real_business_questions_automatically
- does_not_infer_failure_classes_automatically
- does_not_change_runtime_retrieval_defaults
- does_not_enable_query_rewrite_rerank_hybrid_or_graphrag
