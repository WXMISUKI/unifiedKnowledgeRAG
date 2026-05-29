# Evidence Grading Candidate Evaluation

## Summary

| Candidate | Status | Total Cases | Answer-bearing Rate | Related-insufficient | Missing Evidence | Unexpected Evidence | Expected-empty Pass Rate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| citation-match-grader-v1 | candidate | 21 | 1.0000 | 0 | 0 | 0 | 1.0000 |
| source-match-grader-v1 | candidate | 21 | 1.0000 | 0 | 0 | 0 | 1.0000 |

## Candidate Notes

### citation-match-grader-v1

- Description: Strict local grader that requires the expected citation.
- Grading policy: citation_match
- Risk note: Can mark source-level evidence as insufficient when citation granularity changes.
- Risk note: Useful as a strict grounding gate baseline, not a runtime answer gate.
- Decision note: This evaluation is local evidence only and does not filter runtime answers.
- Decision note: Policy: citation_match.
- Decision note: Current seed evidence has no grading failures for this policy.

### source-match-grader-v1

- Description: Looser local grader that accepts the expected source.
- Grading policy: source_match
- Risk note: Can over-credit evidence when the correct source contains multiple topics.
- Risk note: Useful for diagnosing citation granularity problems before reranking.
- Decision note: This evaluation is local evidence only and does not filter runtime answers.
- Decision note: Policy: source_match.
- Decision note: Current seed evidence has no grading failures for this policy.

## Case Results

| Candidate | Case | Category | Label | Reason | Expected Citation | Returned Citations |
| --- | --- | --- | --- | --- | --- | --- |
| citation-match-grader-v1 | refund-delayed-shipping | policy | answer_bearing | Expected citation was returned. | refund_policy_2026#section-3 | refund_policy_2026#section-3, refund_policy_2026#address-change |
| citation-match-grader-v1 | logistics-delay | faq | answer_bearing | Expected citation was returned. | logistics_faq_2026#delay | logistics_faq_2026#delay, logistics_faq_2026#batch-exception |
| citation-match-grader-v1 | empty-moon-warehouse | empty | no_evidence_expected | Expected-empty case returned no evidence. |  |  |
| citation-match-grader-v1 | refund-delivery-paraphrase | paraphrase | answer_bearing | Expected citation was returned. | refund_policy_2026#section-3 | refund_policy_2026#section-3, refund_policy_2026#section-5 |
| citation-match-grader-v1 | refund-evidence-records | evidence | answer_bearing | Expected citation was returned. | refund_policy_2026#section-5 | refund_policy_2026#section-5, refund_policy_2026#appeal-review |
| citation-match-grader-v1 | logistics-carrier-paraphrase | paraphrase | answer_bearing | Expected citation was returned. | logistics_faq_2026#delay | logistics_faq_2026#delay, logistics_faq_2026#lost-package |
| citation-match-grader-v1 | multi-source-after-sales | multi-source | answer_bearing | Expected citation was returned. | refund_policy_2026#section-5 | refund_policy_2026#section-5, refund_policy_2026#appeal-review, logistics_faq_2026#batch-exception |
| citation-match-grader-v1 | refund-customized-exception | exception-policy | answer_bearing | Expected citation was returned. | refund_policy_2026#exception | refund_policy_2026#exception, refund_policy_2026#appeal-review |
| citation-match-grader-v1 | refund-high-value-review | operational-escalation | answer_bearing | Expected citation was returned. | refund_policy_2026#high-value-review | refund_policy_2026#high-value-review, refund_policy_2026#appeal-review |
| citation-match-grader-v1 | refund-address-change-before-shipping | multi-intent | answer_bearing | Expected citation was returned. | refund_policy_2026#address-change | refund_policy_2026#address-change, logistics_faq_2026#lost-package, refund_policy_2026#section-3 |
| citation-match-grader-v1 | logistics-same-city-timeout | sla | answer_bearing | Expected citation was returned. | logistics_faq_2026#same-city-timeout | logistics_faq_2026#same-city-timeout, logistics_faq_2026#batch-exception |
| citation-match-grader-v1 | logistics-lost-package-cross-team | cross-source | answer_bearing | Expected citation was returned. | logistics_faq_2026#lost-package | logistics_faq_2026#lost-package, logistics_faq_2026#batch-exception, logistics_faq_2026#delay |
| citation-match-grader-v1 | logistics-address-intercept | operational-escalation | answer_bearing | Expected citation was returned. | logistics_faq_2026#address-intercept | logistics_faq_2026#address-intercept, logistics_faq_2026#delay |
| citation-match-grader-v1 | refund-appeal-second-review | long-section | answer_bearing | Expected citation was returned. | refund_policy_2026#appeal-review | refund_policy_2026#appeal-review, refund_policy_2026#section-5, refund_policy_2026#section-3 |
| citation-match-grader-v1 | logistics-batch-exception-escalation | long-section | answer_bearing | Expected citation was returned. | logistics_faq_2026#batch-exception | logistics_faq_2026#batch-exception, logistics_faq_2026#lost-package, logistics_faq_2026#delay |
| citation-match-grader-v1 | empty-membership-points | empty | no_evidence_expected | Expected-empty case returned no evidence. |  |  |
| citation-match-grader-v1 | empty-invoice-tax-policy | empty | no_evidence_expected | Expected-empty case returned no evidence. |  |  |
| citation-match-grader-v1 | empty-membership-tier-recovery | empty | no_evidence_expected | Expected-empty case returned no evidence. |  |  |
| citation-match-grader-v1 | empty-coupon-approval | empty | no_evidence_expected | Expected-empty case returned no evidence. |  |  |
| citation-match-grader-v1 | empty-password-reset-email | empty | no_evidence_expected | Expected-empty case returned no evidence. |  |  |
| citation-match-grader-v1 | empty-finance-reconciliation | empty | no_evidence_expected | Expected-empty case returned no evidence. |  |  |
| source-match-grader-v1 | refund-delayed-shipping | policy | answer_bearing | Expected source was returned. | refund_policy_2026#section-3 | refund_policy_2026#section-3, refund_policy_2026#address-change |
| source-match-grader-v1 | logistics-delay | faq | answer_bearing | Expected source was returned. | logistics_faq_2026#delay | logistics_faq_2026#delay, logistics_faq_2026#batch-exception |
| source-match-grader-v1 | empty-moon-warehouse | empty | no_evidence_expected | Expected-empty case returned no evidence. |  |  |
| source-match-grader-v1 | refund-delivery-paraphrase | paraphrase | answer_bearing | Expected source was returned. | refund_policy_2026#section-3 | refund_policy_2026#section-3, refund_policy_2026#section-5 |
| source-match-grader-v1 | refund-evidence-records | evidence | answer_bearing | Expected source was returned. | refund_policy_2026#section-5 | refund_policy_2026#section-5, refund_policy_2026#appeal-review |
| source-match-grader-v1 | logistics-carrier-paraphrase | paraphrase | answer_bearing | Expected source was returned. | logistics_faq_2026#delay | logistics_faq_2026#delay, logistics_faq_2026#lost-package |
| source-match-grader-v1 | multi-source-after-sales | multi-source | answer_bearing | Expected source was returned. | refund_policy_2026#section-5 | refund_policy_2026#section-5, refund_policy_2026#appeal-review, logistics_faq_2026#batch-exception |
| source-match-grader-v1 | refund-customized-exception | exception-policy | answer_bearing | Expected source was returned. | refund_policy_2026#exception | refund_policy_2026#exception, refund_policy_2026#appeal-review |
| source-match-grader-v1 | refund-high-value-review | operational-escalation | answer_bearing | Expected source was returned. | refund_policy_2026#high-value-review | refund_policy_2026#high-value-review, refund_policy_2026#appeal-review |
| source-match-grader-v1 | refund-address-change-before-shipping | multi-intent | answer_bearing | Expected source was returned. | refund_policy_2026#address-change | refund_policy_2026#address-change, logistics_faq_2026#lost-package, refund_policy_2026#section-3 |
| source-match-grader-v1 | logistics-same-city-timeout | sla | answer_bearing | Expected source was returned. | logistics_faq_2026#same-city-timeout | logistics_faq_2026#same-city-timeout, logistics_faq_2026#batch-exception |
| source-match-grader-v1 | logistics-lost-package-cross-team | cross-source | answer_bearing | Expected source was returned. | logistics_faq_2026#lost-package | logistics_faq_2026#lost-package, logistics_faq_2026#batch-exception, logistics_faq_2026#delay |
| source-match-grader-v1 | logistics-address-intercept | operational-escalation | answer_bearing | Expected source was returned. | logistics_faq_2026#address-intercept | logistics_faq_2026#address-intercept, logistics_faq_2026#delay |
| source-match-grader-v1 | refund-appeal-second-review | long-section | answer_bearing | Expected source was returned. | refund_policy_2026#appeal-review | refund_policy_2026#appeal-review, refund_policy_2026#section-5, refund_policy_2026#section-3 |
| source-match-grader-v1 | logistics-batch-exception-escalation | long-section | answer_bearing | Expected source was returned. | logistics_faq_2026#batch-exception | logistics_faq_2026#batch-exception, logistics_faq_2026#lost-package, logistics_faq_2026#delay |
| source-match-grader-v1 | empty-membership-points | empty | no_evidence_expected | Expected-empty case returned no evidence. |  |  |
| source-match-grader-v1 | empty-invoice-tax-policy | empty | no_evidence_expected | Expected-empty case returned no evidence. |  |  |
| source-match-grader-v1 | empty-membership-tier-recovery | empty | no_evidence_expected | Expected-empty case returned no evidence. |  |  |
| source-match-grader-v1 | empty-coupon-approval | empty | no_evidence_expected | Expected-empty case returned no evidence. |  |  |
| source-match-grader-v1 | empty-password-reset-email | empty | no_evidence_expected | Expected-empty case returned no evidence. |  |  |
| source-match-grader-v1 | empty-finance-reconciliation | empty | no_evidence_expected | Expected-empty case returned no evidence. |  |  |
