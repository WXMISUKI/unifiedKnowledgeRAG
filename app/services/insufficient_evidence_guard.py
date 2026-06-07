from __future__ import annotations

from dataclasses import dataclass

from app.models.contracts import EvidenceDocument
from app.services.approved_local_corpus_source_registration import (
    get_approved_local_source,
)


@dataclass(frozen=True)
class InsufficientEvidenceGuardResult:
    documents: list[EvidenceDocument]
    metadata: dict[str, object] | None = None


@dataclass(frozen=True)
class FieldLikeRule:
    id: str
    query_all: tuple[str, ...] = ()
    query_any: tuple[str, ...] = ()
    support_all: tuple[str, ...] = ()
    support_any: tuple[str, ...] = ()


FIELD_LIKE_RULES = [
    FieldLikeRule(
        id="contract_amount",
        query_all=("合同",),
        query_any=("金额", "价款", "总价", "费用", "报价"),
        support_all=("合同",),
        support_any=("金额", "价款", "总价", "费用", "报价", "万元", "元"),
    ),
    FieldLikeRule(
        id="staff_roster",
        query_all=("员工",),
        query_any=("名单", "名录", "花名册", "有哪些"),
        support_any=("员工名单", "人员名单", "员工名录", "人员名录", "花名册"),
    ),
    FieldLikeRule(
        id="contact_phone",
        query_any=("电话", "手机号", "联系方式", "联系人"),
        support_any=("电话", "手机号", "联系方式", "联系人", "联系电话"),
    ),
]


def apply_insufficient_evidence_guard(
    *,
    query: str,
    requested_source_ids: list[str],
    documents: list[EvidenceDocument],
) -> InsufficientEvidenceGuardResult:
    rule = _matching_rule(query)
    if rule is None or not documents or not _is_parser_derived_local_request(requested_source_ids):
        return InsufficientEvidenceGuardResult(documents=documents)

    supported = [document for document in documents if _document_supports_rule(document, rule)]
    if supported:
        if len(supported) == len(documents):
            return InsufficientEvidenceGuardResult(documents=documents)
        return InsufficientEvidenceGuardResult(
            documents=supported,
            metadata=_metadata(
                rule=rule,
                decision="filtered_to_supporting_evidence",
                before_count=len(documents),
                after_count=len(supported),
            ),
        )
    return InsufficientEvidenceGuardResult(
        documents=[],
        metadata=_metadata(
            rule=rule,
            decision="insufficient_evidence",
            before_count=len(documents),
            after_count=0,
        ),
    )


def _matching_rule(query: str) -> FieldLikeRule | None:
    normalized = _normalize(query)
    for rule in FIELD_LIKE_RULES:
        if rule.query_all and not all(term in normalized for term in rule.query_all):
            continue
        if rule.query_any and not any(term in normalized for term in rule.query_any):
            continue
        return rule
    return None


def _document_supports_rule(document: EvidenceDocument, rule: FieldLikeRule) -> bool:
    text = _normalize(f"{document.title} {document.snippet}")
    if rule.support_all and not all(term in text for term in rule.support_all):
        return False
    if rule.support_any and not any(term in text for term in rule.support_any):
        return False
    return True


def _is_parser_derived_local_request(source_ids: list[str]) -> bool:
    if not source_ids:
        return False
    for source_id in source_ids:
        source = get_approved_local_source(source_id)
        if source is None:
            return False
        if source.metadata.get("registered_from") != "local_corpus_caller_handoff":
            return False
    return True


def _metadata(
    *,
    rule: FieldLikeRule,
    decision: str,
    before_count: int,
    after_count: int,
) -> dict[str, object]:
    return {
        "version": "insufficient-evidence-guard-v1",
        "rule_id": rule.id,
        "decision": decision,
        "candidate_count_before": before_count,
        "candidate_count_after": after_count,
        "scope": "parser_derived_local_corpus",
    }


def _normalize(value: str) -> str:
    return "".join(str(value or "").lower().split())
