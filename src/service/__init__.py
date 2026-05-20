from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from src.config import get_settings
from src.data.repo import get_document_database_repo
from src.data.repo.document_db import DocumentDatabaseRepo
from src.service.document_service import DocumentService
from src.service.health import get_health_service
from src.service.ingestion_service import IngestionService
from src.service.rag_service import RagService
from src.service.vectorstore_service import VectorstoreService

_vectorstore_service: VectorstoreService | None = None


def get_vectorstore_service() -> VectorstoreService:
    global _vectorstore_service
    if _vectorstore_service is None:
        _vectorstore_service = VectorstoreService(get_settings())
    return _vectorstore_service


async def get_document_service(
    document_repo: Annotated[DocumentDatabaseRepo, Depends(get_document_database_repo)],
) -> AsyncGenerator[DocumentService]:
    yield DocumentService(document_repo, get_vectorstore_service())


async def get_ingestion_service(
    document_repo: Annotated[DocumentDatabaseRepo, Depends(get_document_database_repo)],
) -> AsyncGenerator[IngestionService]:
    yield IngestionService(document_repo, get_vectorstore_service())


async def get_rag_service() -> AsyncGenerator[RagService]:
    yield RagService(get_vectorstore_service())


__all__ = [
    "get_document_service",
    "get_health_service",
    "get_ingestion_service",
    "get_rag_service",
    "get_vectorstore_service",
]
