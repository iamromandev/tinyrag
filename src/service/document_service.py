from __future__ import annotations

import uuid

from loguru import logger

from src.core.base import BaseService
from src.core.error import Error
from src.data.repo.interface.document import DocumentRepo
from src.data.schema.document import DocumentSchema
from src.service.vectorstore_service import VectorstoreService


class DocumentService(BaseService):
    def __init__(
        self,
        document_repo: DocumentRepo,
        vectorstore_service: VectorstoreService,
    ) -> None:
        super().__init__()
        self._document_repo = document_repo
        self._vectorstore_service = vectorstore_service

    async def list_documents(self) -> list[DocumentSchema]:
        rows = await self._document_repo.list_active()
        return [DocumentSchema.model_validate(row) for row in rows]

    async def delete_document(self, document_id: uuid.UUID) -> None:
        doc = await self._document_repo.get_by_id_active(document_id)
        if doc is None:
            raise Error.not_found(f"Document {document_id} not found")

        await self._vectorstore_service.delete_by_document_id(document_id)
        await self._document_repo.soft_delete(document_id)
        logger.info(f"{self._tag}|delete_document(): deleted {document_id}")
