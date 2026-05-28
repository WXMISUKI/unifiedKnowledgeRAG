from fastapi import APIRouter

from app.config import get_settings
from app.models.contracts import IndexStatusResponse
from app.services.index_lifecycle import get_index_status

router = APIRouter(prefix="/api/indexes")


@router.get("/{source_id}/status", response_model=IndexStatusResponse)
def index_status(source_id: str) -> IndexStatusResponse:
    return get_index_status(source_id, get_settings())
