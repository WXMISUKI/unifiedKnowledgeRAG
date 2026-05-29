# Query Rewrite Candidate Evaluation

## Summary

| Candidate | Status | Total Cases | Rewritten Cases | Rewrite Rate | Expected-empty Rewrites | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| original-query-baseline | baseline | 21 | 0 | 0.0000 | 0 | 1.0000 | 1.0000 | 1.0000 |
| controlled-support-rewrite-v1 | candidate | 21 | 6 | 0.2857 | 0 | 1.0000 | 1.0000 | 1.0000 |

## Candidate Notes

### original-query-baseline

- Description: Original benchmark queries without rewrite.
- Rewrite policy: none
- Risk note: Used as the regression control for any future rewrite strategy.
- Risk note: Does not improve ambiguous or terse user wording.
- Decision note: Baseline candidate preserves every original benchmark query.
- Decision note: Use this as the comparison row for future rewrite strategies.

### controlled-support-rewrite-v1

- Description: Deterministic support-domain rewrite for selected non-empty benchmark cases.
- Rewrite policy: controlled_support_rules
- Risk note: Only rewrites known benchmark cases; not a general production policy.
- Risk note: Expected-empty cases are never rewritten to avoid false positives.
- Risk note: Runtime adoption still requires broader false-positive evidence.
- Decision note: Candidate rewrote 6 benchmark case(s) with deterministic local rules.
- Decision note: No LLM call, hosted provider, or runtime API behavior is introduced.
- Decision note: Expected-empty cases were preserved to protect negative controls.
- Decision note: Current seed evidence does not show a regression against fixture retrieval.

## Case Results

| Candidate | Case | Category | Rewritten | Expected Empty | Hit@K | Citation Match | Empty Handling | Original Query | Rewritten Query |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| original-query-baseline | refund-delayed-shipping | policy | false | false | true | true |  | 客户三天未发货能否退款？ | 客户三天未发货能否退款？ |
| original-query-baseline | logistics-delay | faq | false | false | true | true |  | 物流轨迹二十四小时没有更新怎么办？ | 物流轨迹二十四小时没有更新怎么办？ |
| original-query-baseline | empty-moon-warehouse | empty | false | true | true | true | true | 完全不存在的月球仓库规则 | 完全不存在的月球仓库规则 |
| original-query-baseline | refund-delivery-paraphrase | paraphrase | false | false | true | true |  | 买家等了三天还没有发出包裹，可以走售后退款吗？ | 买家等了三天还没有发出包裹，可以走售后退款吗？ |
| original-query-baseline | refund-evidence-records | evidence | false | false | true | true |  | 处理退款时要保留哪些凭证和记录？ | 处理退款时要保留哪些凭证和记录？ |
| original-query-baseline | logistics-carrier-paraphrase | paraphrase | false | false | true | true |  | 快递信息一天都没变化，应该先找谁确认？ | 快递信息一天都没变化，应该先找谁确认？ |
| original-query-baseline | multi-source-after-sales | multi-source | false | false | true | true |  | 售后同事同时关注退款记录和物流延迟时，应该查哪些资料？ | 售后同事同时关注退款记录和物流延迟时，应该查哪些资料？ |
| original-query-baseline | refund-customized-exception | exception-policy | false | false | true | true |  | 定制商品拆封以后还能无理由退款吗？ | 定制商品拆封以后还能无理由退款吗？ |
| original-query-baseline | refund-high-value-review | operational-escalation | false | false | true | true |  | 五千元以上的高价值退款需要谁复核？ | 五千元以上的高价值退款需要谁复核？ |
| original-query-baseline | refund-address-change-before-shipping | multi-intent | false | false | true | true |  | 客户说还没发货但想改地址，客服应该先退款还是先暂停发货？ | 客户说还没发货但想改地址，客服应该先退款还是先暂停发货？ |
| original-query-baseline | logistics-same-city-timeout | sla | false | false | true | true |  | 同城配送两个小时还没送到，客服先核实什么？ | 同城配送两个小时还没送到，客服先核实什么？ |
| original-query-baseline | logistics-lost-package-cross-team | cross-source | false | false | true | true |  | 承运商确认包裹丢失后，客服要建什么工单并同步哪个团队？ | 承运商确认包裹丢失后，客服要建什么工单并同步哪个团队？ |
| original-query-baseline | logistics-address-intercept | operational-escalation | false | false | true | true |  | 订单已经出库后用户要改收货地址，应该先联系谁拦截？ | 订单已经出库后用户要改收货地址，应该先联系谁拦截？ |
| original-query-baseline | refund-appeal-second-review | long-section | false | false | true | true |  | 客户补充付款凭证和沟通截图后，退款申诉要直接关闭还是提交二线审核？ | 客户补充付款凭证和沟通截图后，退款申诉要直接关闭还是提交二线审核？ |
| original-query-baseline | logistics-batch-exception-escalation | long-section | false | false | true | true |  | 同一承运商一小时内多单轨迹停滞时，客服主管要汇总什么并同步哪个团队？ | 同一承运商一小时内多单轨迹停滞时，客服主管要汇总什么并同步哪个团队？ |
| original-query-baseline | empty-membership-points | empty | false | true | true | true | true | 会员积分兑换失败以后应该怎么补偿？ | 会员积分兑换失败以后应该怎么补偿？ |
| original-query-baseline | empty-invoice-tax-policy | empty | false | true | true | true | true | 企业客户要求开具跨境税务发票时需要哪些资质？ | 企业客户要求开具跨境税务发票时需要哪些资质？ |
| original-query-baseline | empty-membership-tier-recovery | empty | false | true | true | true | true | 会员等级降级后权益如何恢复？ | 会员等级降级后权益如何恢复？ |
| original-query-baseline | empty-coupon-approval | empty | false | true | true | true | true | 优惠券核销码过期后由谁审批？ | 优惠券核销码过期后由谁审批？ |
| original-query-baseline | empty-password-reset-email | empty | false | true | true | true | true | 密码重置邮件收不到的规则是什么？ | 密码重置邮件收不到的规则是什么？ |
| original-query-baseline | empty-finance-reconciliation | empty | false | true | true | true | true | 财务回款对账差异归属哪个流程？ | 财务回款对账差异归属哪个流程？ |
| controlled-support-rewrite-v1 | refund-delayed-shipping | policy | false | false | true | true |  | 客户三天未发货能否退款？ | 客户三天未发货能否退款？ |
| controlled-support-rewrite-v1 | logistics-delay | faq | false | false | true | true |  | 物流轨迹二十四小时没有更新怎么办？ | 物流轨迹二十四小时没有更新怎么办？ |
| controlled-support-rewrite-v1 | empty-moon-warehouse | empty | false | true | true | true | true | 完全不存在的月球仓库规则 | 完全不存在的月球仓库规则 |
| controlled-support-rewrite-v1 | refund-delivery-paraphrase | paraphrase | true | false | true | true |  | 买家等了三天还没有发出包裹，可以走售后退款吗？ | 客户三天未发货可以申请退款，售后专员应核验订单状态和发货记录后处理。 |
| controlled-support-rewrite-v1 | refund-evidence-records | evidence | false | false | true | true |  | 处理退款时要保留哪些凭证和记录？ | 处理退款时要保留哪些凭证和记录？ |
| controlled-support-rewrite-v1 | logistics-carrier-paraphrase | paraphrase | true | false | true | true |  | 快递信息一天都没变化，应该先找谁确认？ | 物流轨迹超过二十四小时未更新时，应先联系承运商确认揽收和中转状态。 |
| controlled-support-rewrite-v1 | multi-source-after-sales | multi-source | false | false | true | true |  | 售后同事同时关注退款记录和物流延迟时，应该查哪些资料？ | 售后同事同时关注退款记录和物流延迟时，应该查哪些资料？ |
| controlled-support-rewrite-v1 | refund-customized-exception | exception-policy | false | false | true | true |  | 定制商品拆封以后还能无理由退款吗？ | 定制商品拆封以后还能无理由退款吗？ |
| controlled-support-rewrite-v1 | refund-high-value-review | operational-escalation | false | false | true | true |  | 五千元以上的高价值退款需要谁复核？ | 五千元以上的高价值退款需要谁复核？ |
| controlled-support-rewrite-v1 | refund-address-change-before-shipping | multi-intent | true | false | true | true |  | 客户说还没发货但想改地址，客服应该先退款还是先暂停发货？ | 用户同时反馈未发货和地址变更，售后专员应先暂停发货，再确认继续履约或退款。 |
| controlled-support-rewrite-v1 | logistics-same-city-timeout | sla | false | false | true | true |  | 同城配送两个小时还没送到，客服先核实什么？ | 同城配送两个小时还没送到，客服先核实什么？ |
| controlled-support-rewrite-v1 | logistics-lost-package-cross-team | cross-source | true | false | true | true |  | 承运商确认包裹丢失后，客服要建什么工单并同步哪个团队？ | 承运商确认包裹丢失后，客服应创建物流异常工单，并同步售后团队评估补发或退款。 |
| controlled-support-rewrite-v1 | logistics-address-intercept | operational-escalation | false | false | true | true |  | 订单已经出库后用户要改收货地址，应该先联系谁拦截？ | 订单已经出库后用户要改收货地址，应该先联系谁拦截？ |
| controlled-support-rewrite-v1 | refund-appeal-second-review | long-section | true | false | true | true |  | 客户补充付款凭证和沟通截图后，退款申诉要直接关闭还是提交二线审核？ | 退款申诉复核场景中，客服应补充原始订单、沟通记录和拒绝理由交由二线复核。 |
| controlled-support-rewrite-v1 | logistics-batch-exception-escalation | long-section | true | false | true | true |  | 同一承运商一小时内多单轨迹停滞时，客服主管要汇总什么并同步哪个团队？ | 批量物流异常需要创建批量异常工单，记录受影响订单范围并通知运营负责人。 |
| controlled-support-rewrite-v1 | empty-membership-points | empty | false | true | true | true | true | 会员积分兑换失败以后应该怎么补偿？ | 会员积分兑换失败以后应该怎么补偿？ |
| controlled-support-rewrite-v1 | empty-invoice-tax-policy | empty | false | true | true | true | true | 企业客户要求开具跨境税务发票时需要哪些资质？ | 企业客户要求开具跨境税务发票时需要哪些资质？ |
| controlled-support-rewrite-v1 | empty-membership-tier-recovery | empty | false | true | true | true | true | 会员等级降级后权益如何恢复？ | 会员等级降级后权益如何恢复？ |
| controlled-support-rewrite-v1 | empty-coupon-approval | empty | false | true | true | true | true | 优惠券核销码过期后由谁审批？ | 优惠券核销码过期后由谁审批？ |
| controlled-support-rewrite-v1 | empty-password-reset-email | empty | false | true | true | true | true | 密码重置邮件收不到的规则是什么？ | 密码重置邮件收不到的规则是什么？ |
| controlled-support-rewrite-v1 | empty-finance-reconciliation | empty | false | true | true | true | true | 财务回款对账差异归属哪个流程？ | 财务回款对账差异归属哪个流程？ |
