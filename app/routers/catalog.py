from fastapi import APIRouter

from app.models.contracts import CatalogResponse
from app.services.source_catalog import list_graphs, list_knowledge_bases

router = APIRouter(prefix="/api")


@router.get("/catalog", response_model=CatalogResponse)
def catalog() -> CatalogResponse:
    return CatalogResponse(
        knowledge_bases=list_knowledge_bases(),
        graphs=list_graphs(),
    )
