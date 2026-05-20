from __future__ import annotations

import uuid

from langchain_core.documents import Document as LcDocument
from langchain_postgres import PGVector
from loguru import logger
from tortoise import Tortoise

from src.config import Settings, get_settings
from src.lib.llm_factory import get_embeddings


class VectorstoreService:
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._store: PGVector | None = None

    def _get_store(self) -> PGVector:
        if self._store is None:
            self._store = PGVector(
                embeddings=get_embeddings(self._settings),
                collection_name=self._settings.collection_name,
                connection=self._settings.langchain_database_url,
                use_jsonb=True,
            )
        return self._store

    def add_chunks(
        self,
        *,
        document_id: uuid.UUID,
        filename: str,
        chunks: list[LcDocument],
    ) -> None:
        store = self._get_store()
        for index, chunk in enumerate(chunks):
            chunk.metadata["document_id"] = str(document_id)
            chunk.metadata["filename"] = filename
            chunk.metadata["chunk_index"] = index
        store.add_documents(chunks)

    def as_retriever(self, *, document_ids: list[uuid.UUID] | None = None):
        search_kwargs: dict = {"k": self._settings.retrieval_top_k}
        if document_ids:
            search_kwargs["filter"] = {
                "document_id": {"$in": [str(doc_id) for doc_id in document_ids]}
            }
        return self._get_store().as_retriever(search_kwargs=search_kwargs)

    async def delete_by_document_id(self, document_id: uuid.UUID) -> None:
        conn = Tortoise.get_connection("default")
        try:
            await conn.execute_query(
                """
                DELETE FROM langchain_pg_embedding e
                USING langchain_pg_collection c
                WHERE e.collection_id = c.uuid
                  AND c.name = $1
                  AND e.cmetadata->>'document_id' = $2
                """,
                [self._settings.collection_name, str(document_id)],
            )
        except Exception as error:
            logger.warning(
                "{}|delete_by_document_id(): {}",
                self.__class__.__name__,
                error,
            )
