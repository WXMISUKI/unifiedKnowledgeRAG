from fastapi import FastAPI

from app.routers import (
    capabilities,
    catalog,
    graph,
    health,
    indexes,
    ingestion,
    provider,
    rag,
)


def create_app() -> FastAPI:
    app = FastAPI(title="unifiedKnowledgeProvider", version="0.1.0")
    app.include_router(health.router)
    app.include_router(capabilities.router)
    app.include_router(catalog.router)
    app.include_router(provider.router)
    app.include_router(ingestion.router)
    app.include_router(indexes.router)
    app.include_router(rag.router)
    app.include_router(graph.router)
    return app


app = create_app()
