# Evidence Grading Candidate Evaluation

## Summary

| Candidate | Status | Total Cases | Answer-bearing Rate | Related-insufficient | Missing Evidence | Unexpected Evidence | Expected-empty Pass Rate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| citation-match-grader-v1 | candidate | 3 | 0.0000 | 1 | 1 | 1 | 0.0000 |
| source-match-grader-v1 | candidate | 3 | 0.3333 | 0 | 1 | 1 | 0.0000 |

## Candidate Notes

### citation-match-grader-v1

- Description: Strict local grader that requires the expected citation.
- Grading policy: citation_match
- Risk note: Can mark source-level evidence as insufficient when citation granularity changes.
- Risk note: Useful as a strict grounding gate baseline, not a runtime answer gate.
- Decision note: This evaluation is local evidence only and does not filter runtime answers.
- Decision note: Policy: citation_match.
- Decision note: 1 case(s) returned related but insufficient evidence.
- Decision note: 1 case(s) missed expected evidence.
- Decision note: 1 expected-empty case(s) returned evidence.

### source-match-grader-v1

- Description: Looser local grader that accepts the expected source.
- Grading policy: source_match
- Risk note: Can over-credit evidence when the correct source contains multiple topics.
- Risk note: Useful for diagnosing citation granularity problems before reranking.
- Decision note: This evaluation is local evidence only and does not filter runtime answers.
- Decision note: Policy: source_match.
- Decision note: 1 case(s) missed expected evidence.
- Decision note: 1 expected-empty case(s) returned evidence.

## Case Results

| Candidate | Case | Category | Label | Reason | Expected Citation | Returned Citations |
| --- | --- | --- | --- | --- | --- | --- |
| citation-match-grader-v1 | stress-refund-source-but-wrong-citation | insufficient-evidence | related_insufficient | Expected source was returned but expected citation was missing. | refund_policy_2026#appeal-review | refund_policy_2026#section-3, refund_policy_2026#address-change |
| citation-match-grader-v1 | stress-missing-evidence-unmatched-vocabulary | missing-evidence | missing_evidence | Expected source and citation were not returned. | refund_policy_2026#section-5 |  |
| citation-match-grader-v1 | stress-unexpected-evidence-membership-refund-overlap | unexpected-evidence | unexpected_evidence | Expected-empty case returned evidence. |  | refund_policy_2026#high-value-review, refund_policy_2026#appeal-review |
| source-match-grader-v1 | stress-refund-source-but-wrong-citation | insufficient-evidence | answer_bearing | Expected source was returned. | refund_policy_2026#appeal-review | refund_policy_2026#section-3, refund_policy_2026#address-change |
| source-match-grader-v1 | stress-missing-evidence-unmatched-vocabulary | missing-evidence | missing_evidence | No evidence was returned for a non-empty case. | refund_policy_2026#section-5 |  |
| source-match-grader-v1 | stress-unexpected-evidence-membership-refund-overlap | unexpected-evidence | unexpected_evidence | Expected-empty case returned evidence. |  | refund_policy_2026#high-value-review, refund_policy_2026#appeal-review |
