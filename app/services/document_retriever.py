import re
from dataclasses import dataclass
from pathlib import Path

from app.models.contracts import EvidenceDocument
from app.services.approved_local_corpus_source_registration import (
    get_approved_local_source,
    list_approved_local_sources,
)
from app.services.source_catalog import knowledge_base_exists


@dataclass(frozen=True)
class DocumentChunk:
    source_id: str
    document_id: str
    title: str
    text: str
    citation: str
    source_path: str | None = None


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
        source_id="refund_policy_docs",
        document_id="refund_policy_2026",
        title="精确退款编码",
        text=(
            "政策编号 RFD-2026-003 适用于三天未发货退款复核；"
            "售后专员需填写表单 AF-REFUND-02，并关联原订单编号和付款凭证。"
        ),
        citation="refund_policy_2026#exact-refund-code",
    ),
    DocumentChunk(
        source_id="refund_policy_docs",
        document_id="refund_policy_2026",
        title="退款例外规则",
        text="定制商品、已拆封影响二次销售的商品，除质量问题外不支持无理由退款。",
        citation="refund_policy_2026#exception",
    ),
    DocumentChunk(
        source_id="refund_policy_docs",
        document_id="refund_policy_2026",
        title="高价值退款复核",
        text="高价值订单退款超过五千元时，需要售后主管复核并在工单中记录复核意见。",
        citation="refund_policy_2026#high-value-review",
    ),
    DocumentChunk(
        source_id="refund_policy_docs",
        document_id="refund_policy_2026",
        title="未发货地址变更",
        text="如果用户同时反馈未发货和地址变更，售后专员应先暂停发货，再确认是否继续履约或退款。",
        citation="refund_policy_2026#address-change",
    ),
    DocumentChunk(
        source_id="refund_policy_docs",
        document_id="refund_policy_2026",
        title="退款申诉复核",
        text=(
            "退款申诉复核场景中，如果客户已经补充上传付款凭证、客服沟通截图、商品问题照片和物流签收记录，"
            "售后专员不得直接关闭工单，应先在申诉备注中逐项核对证据完整性，再提交二线审核；"
            "二线审核需要在两个工作日内给出维持原判、补充举证或重新退款的结论，并把结论写入申诉处理记录，便于后续客服解释。"
        ),
        citation="refund_policy_2026#appeal-review",
    ),
    DocumentChunk(
        source_id="logistics_faq",
        document_id="logistics_faq_2026",
        title="物流常见问题",
        text="物流轨迹超过二十四小时未更新时，应先联系承运商确认揽收和中转状态。",
        citation="logistics_faq_2026#delay",
    ),
    DocumentChunk(
        source_id="logistics_faq",
        document_id="logistics_faq_2026",
        title="同城配送超时",
        text="同城即时配送超过两小时未送达时，客服应优先核实骑手位置和收件人联系方式。",
        citation="logistics_faq_2026#same-city-timeout",
    ),
    DocumentChunk(
        source_id="logistics_faq",
        document_id="logistics_faq_2026",
        title="包裹丢失协同",
        text="承运商确认包裹丢失后，客服应创建物流异常工单，并同步售后团队评估补发或退款。",
        citation="logistics_faq_2026#lost-package",
    ),
    DocumentChunk(
        source_id="logistics_faq",
        document_id="logistics_faq_2026",
        title="地址修改拦截",
        text="用户要求修改收货地址时，如果订单已经出库，应先联系承运商拦截，无法拦截时需要提示用户关注派送失败退回。",
        citation="logistics_faq_2026#address-intercept",
    ),
    DocumentChunk(
        source_id="logistics_faq",
        document_id="logistics_faq_2026",
        title="批量物流异常",
        text=(
            "批量物流异常处理中，如果同一承运商在一个小时内出现五单以上轨迹停滞、派送失败或网点滞留，"
            "客服主管应先汇总受影响订单、承运商名称、最近一次轨迹时间和客户承诺时效，再创建批量异常工单；"
            "工单需要同步物流运营团队判断是否触发承运商升级沟通，同时通知售后团队准备补发、退款或安抚方案，避免单个客服重复联系造成口径不一致。"
        ),
        citation="logistics_faq_2026#batch-exception",
    ),
    DocumentChunk(
        source_id="logistics_faq",
        document_id="logistics_faq_2026",
        title="精确物流标识",
        text=(
            "工作流缩写 LST-BATCH-OPS 是批量物流异常升级代号；"
            "样例订单 ORD-ZS-2026-0007 用于演示承运商网点滞留后的拦截和升级凭据。"
        ),
        citation="logistics_faq_2026#exact-logistics-id",
    ),
]


STOP_TOKENS = {
    "客户",
    "用户",
    "要求",
    "户要",
    "时需",
    "需要",
    "应该",
    "哪些",
    "怎么",
    "以后",
    "失败",
}

MIN_LEXICAL_MATCH_SCORE = 0.2


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
    for document in DOCUMENTS + _approved_local_documents():
        if document.source_id not in knowledge_base_ids:
            continue
        text_tokens = _tokenize(document.text)
        overlap = query_tokens & text_tokens
        score = _score_from_overlap(query_tokens, overlap)
        if _is_retrievable_match(score=score, overlap=overlap):
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
            metadata={
                "source_path": document.source_path or _source_path_for(document.source_id),
                "chunk_id": _chunk_id_for(document.citation),
                "chunking_strategy": "fixture-evidence-v1",
                "citation_anchor": document.citation,
            },
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
    overlap = query_tokens & text_tokens
    return _score_from_overlap(query_tokens, overlap)


def _score_from_overlap(query_tokens: set[str], overlap: set[str]) -> float:
    if not query_tokens:
        return 0.0
    if not overlap:
        return 0.0
    return len(overlap) / len(query_tokens)


def _is_retrievable_match(*, score: float, overlap: set[str]) -> bool:
    if score <= 0:
        return False
    if score >= MIN_LEXICAL_MATCH_SCORE:
        return True
    return _has_exact_alphanumeric_overlap(overlap)


def _has_exact_alphanumeric_overlap(overlap: set[str]) -> bool:
    return any(re.fullmatch(r"[a-z0-9]+", token) for token in overlap)


def _tokenize(value: str) -> set[str]:
    normalized = re.sub(r"\s+", "", value.lower())
    tokens = set(re.findall(r"[a-z0-9]+", value.lower()))
    tokens.update(_cjk_bigrams(normalized))
    return tokens - STOP_TOKENS


def _cjk_bigrams(value: str) -> set[str]:
    cjk_chars = [char for char in value if "\u4e00" <= char <= "\u9fff"]
    return {
        "".join(cjk_chars[index : index + 2])
        for index in range(max(len(cjk_chars) - 1, 0))
    }


def _source_path_for(source_id: str) -> str:
    approved_source = get_approved_local_source(source_id)
    if approved_source is not None:
        return approved_source.source_path
    return f"app/data/sources/{source_id}.md"


def _chunk_id_for(citation: str) -> str:
    return citation.split("#", maxsplit=1)[-1]


def _approved_local_documents() -> list[DocumentChunk]:
    documents: list[DocumentChunk] = []
    for source in list_approved_local_sources():
        source_path = source.source_path
        path = Path(source_path)
        if not path.exists():
            continue
        for index, chunk in enumerate(
            _markdown_chunks(path.read_text(encoding="utf-8")),
            start=1,
        ):
            documents.append(
                DocumentChunk(
                    source_id=source.source_id,
                    document_id=source.document_id,
                    title=source.title,
                    text=chunk,
                    citation=f"{source.document_id}#chunk-{index}",
                    source_path=source_path,
                )
            )
    return documents


def _markdown_chunks(text: str) -> list[str]:
    chunks: list[str] = []
    current_lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if current_lines:
                chunks.append(" ".join(current_lines))
                current_lines = []
            continue
        if line.startswith("#"):
            continue
        current_lines.append(line)
    if current_lines:
        chunks.append(" ".join(current_lines))
    return chunks
