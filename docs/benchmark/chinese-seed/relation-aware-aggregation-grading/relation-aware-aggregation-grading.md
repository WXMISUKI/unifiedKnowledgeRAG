# Evidence Grading Candidate Evaluation

## Summary

| Candidate | Status | Total Cases | Answer-bearing Rate | Related-insufficient | Relation-unsupported | Missing Evidence | Unexpected Evidence | Expected-empty Pass Rate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| relation-aware-aggregation-grader-v1 | candidate | 2 | 1.0000 | 0 | 1 | 0 | 0 | 1.0000 |

## Candidate Notes

### relation-aware-aggregation-grader-v1

- Description: Deterministic local grader for multi-chunk aggregation outputs that separates unsupported relationship questions from answer-bearing evidence.
- Grading policy: relation_aware_identifier
- Risk note: Uses narrow local relation markers and is not a production semantic grader.
- Risk note: Does not call an LLM, reranker, or graph store.
- Risk note: Runtime retrieval and answer behavior remain unchanged.
- Decision note: This evaluation is local evidence only and does not filter runtime answers.
- Decision note: Policy: relation_aware_identifier.
- Decision note: 1 expected-empty relation case(s) were labeled unsupported rather than answer-bearing.

## Case Results

| Candidate | Case | Category | Label | Reason | Expected Citation | Returned Citations |
| --- | --- | --- | --- | --- | --- | --- |
| relation-aware-aggregation-grader-v1 | split-chunk-refund-policy-and-form | split-chunk-identifier | answer_bearing | Expected citation was returned. | split_refund_policy_2026#form-code | split_refund_policy_2026#form-code, split_refund_policy_2026#policy-code |
| relation-aware-aggregation-grader-v1 | multi-chunk-empty-unsupported-form-policy-link | multi-chunk-aggregation-empty | relation_unsupported | Returned evidence contains identifiers but does not prove the requested relationship. |  | split_refund_policy_2026#form-code, split_refund_policy_2026#policy-code |
