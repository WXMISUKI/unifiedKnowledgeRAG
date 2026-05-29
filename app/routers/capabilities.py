from fastapi import APIRouter

from app.config import get_settings
from app.models.contracts import CapabilitiesResponse, Capability, CapabilityInvocation
from app.services.rag_answer_orchestrator import answer_composer_readiness

router = APIRouter(prefix="/api")


@router.get("/capabilities", response_model=CapabilitiesResponse)
def capabilities() -> CapabilitiesResponse:
    answer_status, _answer_reason, _answer_backend, _answer_model = answer_composer_readiness(
        get_settings()
    )
    return CapabilitiesResponse(
        capabilities=[
            Capability(
                id="knowledge.rag.retrieve",
                status="ready",
                description="Retrieve compact document evidence with stable citations.",
                invocation=CapabilityInvocation(method="POST", path="/api/rag/retrieve"),
            ),
            Capability(
                id="knowledge.rag.answer",
                status=answer_status,
                description=(
                    "Compose cited document RAG answers with evidence gating and "
                    "configurable composer boundaries."
                ),
                invocation=CapabilityInvocation(method="POST", path="/api/rag/answer"),
            ),
            Capability(
                id="knowledge.graph.query",
                status="planned",
                description="Graph query contract boundary; execution is deferred.",
                invocation=CapabilityInvocation(method="POST", path="/api/graph/query"),
            ),
        ]
    )
