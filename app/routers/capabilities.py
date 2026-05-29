from fastapi import APIRouter

from app.models.contracts import CapabilitiesResponse, Capability, CapabilityInvocation

router = APIRouter(prefix="/api")


@router.get("/capabilities", response_model=CapabilitiesResponse)
def capabilities() -> CapabilitiesResponse:
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
                status="ready",
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
