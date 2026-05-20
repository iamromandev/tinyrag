from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from src.data.db.model import Document


class DocumentRepo(ABC):
    @abstractmethod
    async def create_document(
        self,
        *,
        filename: str,
        content_type: str,
        size_bytes: int,
        chunk_count: int = 0,
    ) -> Document:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id_active(self, document_id: uuid.UUID) -> Document | None:
        raise NotImplementedError

    @abstractmethod
    async def list_active(self) -> list[Document]:
        raise NotImplementedError

    @abstractmethod
    async def soft_delete(self, document_id: uuid.UUID) -> bool:
        raise NotImplementedError
