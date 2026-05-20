from __future__ import annotations

import uuid

from src.core.base import BaseRepo
from src.data.db.model import Document
from src.data.repo.interface.document import DocumentRepo


class DocumentDatabaseRepo(BaseRepo[Document], DocumentRepo):
    def __init__(self) -> None:
        super().__init__(Document)

    async def create_document(
        self,
        *,
        filename: str,
        content_type: str,
        size_bytes: int,
        chunk_count: int = 0,
    ) -> Document:
        return await self.create(
            filename=filename,
            content_type=content_type,
            size_bytes=size_bytes,
            chunk_count=chunk_count,
        )

    async def get_by_id_active(self, document_id: uuid.UUID) -> Document | None:
        return await self.get_one(id=document_id, deleted_at__isnull=True)

    async def list_active(self) -> list[Document]:
        return await Document.get_active().order_by("-created_at")

    async def soft_delete(self, document_id: uuid.UUID) -> bool:
        doc = await self.get_by_id_active(document_id)
        if doc is None:
            return False
        await doc.soft_delete()
        return True
