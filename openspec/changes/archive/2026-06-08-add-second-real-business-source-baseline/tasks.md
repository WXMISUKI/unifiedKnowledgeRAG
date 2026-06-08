## 1. Spec And Fixture Scope

- [x] 1.1 Finalize the OpenSpec proposal, design, and spec deltas for second-source aggregate baseline expansion
- [x] 1.2 Define the second real business source cases for `refund_policy_docs` with positive and negative controls

## 2. Aggregate Baseline Implementation

- [x] 2.1 Update the checked-in aggregate real-business case fixture to include `refund_policy_docs`
- [x] 2.2 Refresh the aggregate export and keep existing single-source compatibility intact

## 3. Verification

- [x] 3.1 Add or update focused tests for second-source aggregate `go`, `review`, and `blocked` behavior
- [x] 3.2 Run focused pytest and `openspec validate --all --strict`

## 4. Documentation And Closure

- [x] 4.1 Refresh roadmap/progress documentation with the second-source baseline outcome and next-step rule
- [x] 4.2 Archive the OpenSpec change after verification while keeping runtime defaults unchanged
