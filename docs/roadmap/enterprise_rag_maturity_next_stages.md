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

The current immediate stage is no longer a new provider feature slice. It is a phase-closure and hold-state stage:

`docs/progress/provider-phase-closure-summary.md`

This means the project should treat the current provider baseline as closed enough for its present lightweight purpose, and avoid continuing provider-side feature expansion just because more RAG techniques exist.

After that closure, the most practical next slice inside this repository is not another provider capability. It is stabilizing the caller-side live trial outcome input contract so real feedback can flow back into provider-side trigger decisions with less ambiguity.

The current execution entrypoint after that contract is now:

`docs/integration/myprivateagent-live-trial-outcome-feedback/caller-trial-feedback-runbook.md`

Post-closure work should now be read as an ordered sequence:

1. caller-side trial access review
2. caller-side trial execution
3. caller-side trial outcome export
4. provider-side Phase 25 feedback consumption
5. trigger-based reopen or continued hold-state

The stage-2 execution aid for that sequence is now:

`docs/integration/myprivateagent-live-trial-outcome-feedback/caller-trial-execution-task-pack.md`

The stage-3 decision entrypoint for that sequence is now:

`docs/integration/myprivateagent-live-trial-outcome-feedback/phase25-followup-decision-matrix.md`

Stage 1 in `MyPrivateAgent` is closed for the current local company profile trial. Stage 2 in `unifiedKnowledgeRAG` is closed for the local approved-source ingestion loop. Stage 3 boundary definition, Stage 3b parser-artifact-to-local-ingestion loop, and the local PDF parser provider bridge are closed for the current local company-profile trial. The current practical state is: a real local PDF can be parsed by an operator-started PaddleOCR service, normalized into a parser artifact, and ingested through the existing local RAG loop with `decision=go`.

The current MyPrivateAgent real business trial also returns `go` for the company-profile PDF: answerable business questions produce cited answers, and the negative-control refund-policy question returns `insufficient_evidence` without citations. This closes the current local usability loop.

The next provider-side maturity slice has already converted the current real trial into reusable quality measurement:

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

The current aggregate report is `go` with `source_count=3`, `case_count=12`, `hit_rate=1.0`, `citation_match_rate=1.0`, and `empty_handling_rate=1.0`. It now covers `company_profile_2025_trial`, `refund_policy_docs`, and `logistics_faq`. The third source adds workflow/process questions, exact-term identifier questions, and a new expected-empty negative control without changing runtime defaults.

Because the aggregate baseline is now back to `go` across three real business sources, the next provider action is not to introduce advanced retrieval strategy changes. The next narrow gate is to keep expanding real business documents or accepted failed-question packs until a new accepted failure class appears. Advanced RAG strategy changes remain unpromoted until that concrete failure evidence exists.

## Real Failed Question Pack Baseline

The local operator entrypoint is:

`python scripts/export_real_failed_question_pack_golden_cases.py`

It writes:

- `docs/local-run/business-rag-golden-cases/real-failed-question-pack.json`
- `docs/local-run/business-rag-golden-cases/real-failed-question-pack.md`

The current failed-question pack report is `review` with `source_count=3`, `case_count=6`, `hit_rate=1.0`, `citation_match_rate=1.0`, and `empty_handling_rate=0.6667`. It intentionally collects difficult, failed, or boundary real-business questions separately from the passing aggregate breadth baseline. The first pack exposes one concrete `query_mismatch`-like review candidate on `refund_policy_docs`: `退款政策中有哪些公司部门？` currently returns irrelevant exact-term evidence instead of failing closed.

Because this failure pack now exists, the next provider action is no longer “keep adding breadth only.” The next narrow gate is to confirm whether this review candidate is accepted as a real failure class and, if so, to open a focused hardening slice for that class rather than promoting advanced retrieval strategies broadly.

## Refund Organization Confirmation Baseline

The local operator entrypoint is:

`python scripts/export_refund_organization_negative_control_confirmation.py`

It writes:

- `docs/local-run/business-rag-golden-cases/refund-organization-negative-control-confirmation.json`
- `docs/local-run/business-rag-golden-cases/refund-organization-negative-control-confirmation.md`

The current confirmation report is `review` with `variant_count=8`, `expected_empty_variant_count=5`, `answerable_variant_count=3`, `expected_empty_review_count=2`, and `answerable_pass_count=3`. The confirmed verdict is `confirmed_negative_control_variant`, not a broad query-mismatch promotion signal. Two refund organization-style negative controls still leak `refund_policy_2026#exact-refund-code`, while the three role/responsibility positives remain answerable.

Because this confirmation slice is now complete, the next provider action is to open a narrow refund negative-control hardening scope review, not to introduce query rewrite, rerank, hybrid retrieval, or GraphRAG. The confirmation baseline raises the decision quality of the next slice while keeping runtime defaults unchanged.

## Source Evaluation Pack Catalog

The local operator entrypoint is:

`python scripts/export_source_evaluation_pack_catalog.py`

It writes:

- `docs/local-run/business-rag-golden-cases/source-evaluation-pack-catalog.json`
- `docs/local-run/business-rag-golden-cases/source-evaluation-pack-catalog.md`

The current catalog report is `review` with `pack_count=4`, `available_pack_count=4`, `baseline_pack_count=2`, `failed_question_pack_count=1`, and `confirmation_pack_count=1`. It gives the provider a single evidence-only overview over current baseline, failed-question, and confirmation gates without changing the underlying evaluation logic.

Because this catalog slice is now complete, the next provider action should shift from a specific refund case toward generalized evaluation-pack templating for future sources. The provider now has a common gate index, so the next narrow improvement should be lowering the cost of bringing new sources into the same baseline / failed-pack / confirmation rhythm, not promoting advanced retrieval strategies.

## Source Evaluation Pack Onboarding

The local operator entrypoint is:

`python scripts/export_source_evaluation_pack_onboarding.py --source-id source_template_example`

It writes:

- `docs/local-run/business-rag-golden-cases/onboarding/source_template_example/baseline-pack.fixture.template.json`
- `docs/local-run/business-rag-golden-cases/onboarding/source_template_example/failed-question-pack.fixture.template.json`
- `docs/local-run/business-rag-golden-cases/onboarding/source_template_example/confirmation-pack.fixture.template.json`
- `docs/local-run/business-rag-golden-cases/onboarding/source_template_example/source-evaluation-pack-onboarding.json`
- `docs/local-run/business-rag-golden-cases/onboarding/source_template_example/source-evaluation-pack-onboarding.md`

The current onboarding report is a template-only scaffold with `template_count=3` and pack coverage for `baseline_pack`, `failed_question_pack`, and `confirmation_pack`. It does not run evaluation or infer business questions automatically. Its purpose is to make future source onboarding cheaper and more consistent before any source-specific retrieval changes are considered.

Because this onboarding slice is now complete, the next provider action should be to validate the template-driven path on one additional real source or to add a light registration/discovery bridge from onboarding outputs into the catalog. Advanced retrieval strategies still remain outside scope.

## Split Refund Onboarding Validation

The local operator entrypoint is:

`python scripts/export_split_refund_onboarding_validation.py`

It writes:

- `docs/local-run/business-rag-golden-cases/onboarding/split_refund_policy_docs/source-evaluation-pack-onboarding.json`
- `docs/local-run/business-rag-golden-cases/onboarding/split_refund_policy_docs/baseline-pack.fixture.json`
- `docs/local-run/business-rag-golden-cases/onboarding/split_refund_policy_docs/split-refund-local-business-rag-golden-cases.json`
- `docs/local-run/business-rag-golden-cases/onboarding/split_refund_policy_docs/split-refund-local-business-rag-golden-cases.md`

The current validation report for `split_refund_policy_docs` is `go` with `case_count=3`, `hit_rate=1.0`, `citation_match_rate=1.0`, and `empty_handling_rate=1.0`. This confirms that the template-driven onboarding path is not just a scaffold: a new real source can enter the provider's local baseline evaluation path with only minimal provider visibility additions.

Because this validation slice is now complete, the next provider action should be either to repeat the same template path on a second new real source or to add a light onboarding-to-catalog bridge. Retrieval strategy promotion still remains outside scope.

## Third Distinct Real Source Onboarding Validation

The local operator entrypoint is:

`python scripts/export_invoice_policy_onboarding_validation.py`

It writes:

- `docs/local-run/business-rag-golden-cases/onboarding/invoice_policy_faq/source-evaluation-pack-onboarding.json`
- `docs/local-run/business-rag-golden-cases/onboarding/invoice_policy_faq/baseline-pack.fixture.json`
- `docs/local-run/business-rag-golden-cases/onboarding/invoice_policy_faq/invoice-policy-local-business-rag-golden-cases.json`
- `docs/local-run/business-rag-golden-cases/onboarding/invoice_policy_faq/invoice-policy-local-business-rag-golden-cases.md`

The current validation report for `invoice_policy_faq` is `go` with `case_count=3`, `hit_rate=1.0`, `citation_match_rate=1.0`, and `empty_handling_rate=1.0`. This extends the onboarding proof from workflow/policy snippets to a third, more rule-oriented markdown source type without changing runtime defaults or adding source-specific retrieval logic.

Because this third-source validation slice is now complete, the next provider action should still stay on generalized provider usability: either add one more clearly distinct real source type, or add a light evidence-only bridge that helps onboarding outputs surface in catalog/discovery views. Retrieval strategy promotion remains outside scope until repeated accepted failure classes appear.

## Source Onboarding Catalog Discovery Bridge

The local operator entrypoint is:

`python scripts/export_source_onboarding_catalog.py`

It writes:

- `docs/local-run/business-rag-golden-cases/source-onboarding-catalog.json`
- `docs/local-run/business-rag-golden-cases/source-onboarding-catalog.md`

The current onboarding catalog report is `go` with `source_count=3`, `ready_source_count=2`, and `template_only_source_count=1`. It gives the provider a single evidence-only discovery view over existing onboarding sources without registering them into runtime, without expanding the main aggregate baseline, and without changing retrieval defaults.

Because this discovery bridge slice is now complete, the next provider action should stay in the same lightweight direction: either fill the remaining template-only onboarding example with a real baseline fixture, or add a very small evidence-only bridge from this onboarding catalog into existing pack-level discovery. Retrieval strategy promotion remains outside scope.

## Pack Catalog Onboarding Summary Bridge

The local operator entrypoint remains:

`python scripts/export_source_evaluation_pack_catalog.py`

It now also reads:

- `docs/local-run/business-rag-golden-cases/source-onboarding-catalog.json`

The refreshed pack catalog still returns `review` because the failed-question and confirmation packs remain `review`, but it now also exposes onboarding maturity summary with `onboarding_source_count=3`, `onboarding_ready_source_count=2`, and `onboarding_template_only_source_count=1`. This keeps pack-level discovery and source-onboarding discovery connected without changing pack decision semantics, runtime defaults, source registration, or aggregate-baseline expansion.

Because this bridge slice is now complete, the next provider action should remain lightweight and evidence-first: either turn the remaining template-only onboarding example into a real minimal baseline fixture, or wait for a repeated cross-source failed-question class before opening any hardening slice. Retrieval strategy promotion remains outside scope.

## Real Template Onboarding Example

The local operator entrypoint is:

`python scripts/export_source_template_onboarding_validation.py`

It writes:

- `docs/local-run/business-rag-golden-cases/onboarding/source_template_example/baseline-pack.fixture.json`
- `docs/local-run/business-rag-golden-cases/onboarding/source_template_example/source-template-local-business-rag-golden-cases.json`
- `docs/local-run/business-rag-golden-cases/onboarding/source_template_example/source-template-local-business-rag-golden-cases.md`

The promoted `source_template_example` validation report is now `go` with `case_count=3`, `hit_rate=1.0`, `citation_match_rate=1.0`, and `empty_handling_rate=1.0`. This closes the last template-only onboarding example by turning it into a real minimal baseline example without expanding the main aggregate baseline or changing runtime defaults.

Because this example-promotion slice is now complete, the provider should now enter an explicit hold-state rather than continue polishing onboarding mechanics. Future reopen decisions should reference `docs/progress/provider-phase-closure-summary.md` first.

## Provider Next-Step Trigger Contract

The current provider state should now be treated as:

`paused_for_provider_feature_expansion_until_stronger_trigger_appears`

This means the default next action is no longer "find one more provider slice." Instead, future provider-side work should reopen only when one of these trigger classes appears:

- `real_caller_feedback_trigger`
- `provider_owned_gap_trigger`
- `repeated_cross_source_failure_class_trigger`
- `runtime_strategy_evaluation_trigger`

Trigger interpretation:

- `real_caller_feedback_trigger`: a real caller trial exposes a concrete provider-owned gap
- `provider_owned_gap_trigger`: the problem clearly belongs to provider evidence/retrieval/citation behavior rather than caller orchestration
- `repeated_cross_source_failure_class_trigger`: failed-question evidence shows a repeated accepted failure class across more than one source
- `runtime_strategy_evaluation_trigger`: repeated real failure evidence explicitly justifies evaluating query rewrite, rerank, hybrid retrieval, GraphRAG, or another advanced strategy

The following do **not** reopen provider-side work by default:

- final answer policy
- source-to-agent binding policy
- permissions / approvals
- audit governance
- caller orchestration or control-plane concerns

These remain outside this repository's lightweight provider scope.

## Current Closure Decision

The current phase-closure decision is:

`hold current provider baseline and wait for stronger reopen triggers`

This decision is based on three facts:

- provider usability closure is already in place
- onboarding and evidence discovery closure is already in place
- advanced RAG strategies still have no repeated real failure evidence that justifies promotion or even candidate implementation inside the provider by default

So the correct next action for this repository is not to continue feature expansion. It is to keep the current baseline understandable, maintainable, and ready for the next real trigger.
