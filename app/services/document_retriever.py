import re
from dataclasses import dataclass

from app.models.contracts import EvidenceDocument
from app.services.source_catalog import knowledge_base_exists


@dataclass(frozen=True)
class DocumentChunk:
    source_id: str
    document_id: str
    title: str
    text: str
    citation: str


DOCUMENTS = [
    DocumentChunk(
        source_id="refund_policy_docs",
        document_id="refund_policy_2026",
        title="售后退款规则",
        text="客户三天未发货可以申请退款，售后专员应核验订单状态和发货记录后处理。",
        citation="refund_policy_2026#section-3",
    ),
    DocumentChunk(
        source_id="refund_policy_docs",
        document_id="refund_policy_2026",
        title="退款凭证规则",
        text="退款处理需要保留订单编号、付款记录、售后沟通记录和处理人信息。",
        citation="refund_policy_2026#section-5",
    ),
    DocumentChunk(
        source_id="logistics_faq",
        document_id="logistics_faq_2026",
        title="物流常见问题",
        text="物流轨迹超过二十四小时未更新时，应先联系承运商确认揽收和中转状态。",
        citation="logistics_faq_2026#delay",
    ),
]


def retrieve(
    query: str,
    knowledge_base_ids: list[str],
    top_k: int,
) -> tuple[list[str], list[EvidenceDocument]]:
    unknown_sources = [
        source_id for source_id in knowledge_base_ids if not knowledge_base_exists(source_id)
    ]
    if unknown_sources:
        return unknown_sources, []

    query_tokens = _tokenize(query)
    scored_documents = []
    for document in DOCUMENTS:
        if document.source_id not in knowledge_base_ids:
            continue
        score = _score(query_tokens, document.text)
        if score > 0:
            scored_documents.append((score, document))

    scored_documents.sort(key=lambda item: item[0], reverse=True)
    documents = [
        EvidenceDocument(
            source_id=document.source_id,
            document_id=document.document_id,
            title=document.title,
            snippet=document.text,
            score=round(score, 4),
            citation=document.citation,
        )
        for score, document in scored_documents[:top_k]
    ]
    return [], documents


def build_answer_context(documents: list[EvidenceDocument]) -> str:
    if not documents:
        return ""
    context_parts = [
        f"[{document.citation}] {document.snippet}" for document in documents[:3]
    ]
    return "\n".join(context_parts)


def _score(query_tokens: set[str], text: str) -> float:
    text_tokens = _tokenize(text)
    if not query_tokens or not text_tokens:
        return 0.0
    overlap = query_tokens & text_tokens
    if not overlap:
        return 0.0
    return len(overlap) / len(query_tokens)


def _tokenize(value: str) -> set[str]:
    normalized = re.sub(r"\s+", "", value.lower())
    tokens = set(re.findall(r"[a-z0-9]+", value.lower()))
    tokens.update(_cjk_bigrams(normalized))
    return tokens


def _cjk_bigrams(value: str) -> set[str]:
    cjk_chars = [char for char in value if "\u4e00" <= char <= "\u9fff"]
    return {
        "".join(cjk_chars[index : index + 2])
        for index in range(max(len(cjk_chars) - 1, 0))
    }
