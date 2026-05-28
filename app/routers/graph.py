from fastapi import APIRouter

from app.models.contracts import (
    GraphQueryRequest,
    GraphQueryResponse,
    GraphSchemasResponse,
    ProviderError,
)
from app.services.source_catalog import list_graphs

router = APIRouter(prefix="/api/graph")


@router.get("/schemas", response_model=GraphSchemasResponse)
def schemas() -> GraphSchemasResponse:
    return GraphSchemasResponse(graphs=list_graphs())


@router.post("/query", response_model=GraphQueryResponse)
def query_graph(request: GraphQueryRequest) -> GraphQueryResponse:
    return GraphQueryResponse(
        ok=False,
        error=ProviderError(
            code="GRAPH_NOT_IMPLEMENTED",
            message=f"Graph query execution is not implemented for graph_id '{request.graph_id}' in this slice.",
        ),
    )
