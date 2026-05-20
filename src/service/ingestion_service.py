from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

from src.config import Settings, get_settings
from src.core.base import BaseService
from src.core.error import Error
from src.data.repo.interface.document import DocumentRepo
from src.data.schema.document import UploadResponse
from src.lib.document_loader import ALLOWED_EXTENSIONS, load_documents_from_path
from src.service.vectorstore_service import VectorstoreService


class IngestionService(BaseService):
    def __init__(
        self,
        document_repo: DocumentRepo,
        vectorstore_service: VectorstoreService,
        settings: Settings | None = None,
    ) -> None:
        super().__init__()
        self._document_repo = document_repo
        self._vectorstore_service = vectorstore_service
        self._settings = settings or get_settings()

    async def ingest_upload(self, file: UploadFile) -> UploadResponse:
        if not file.filename:
            raise Error.bad_request("Filename is required")

        suffix = Path(file.filename).suffix.lower()
        if suffix not in ALLOWED_EXTENSIONS:
            raise Error.bad_request(
                f"Unsupported file type '{suffix}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            )

        content = await file.read()
        if not content:
            raise Error.bad_request("Uploaded file is empty")
        if len(content) > self._settings.max_upload_bytes:
            raise Error.bad_request(
                f"File exceeds maximum size of {self._settings.max_upload_bytes} bytes"
            )

        content_type = file.content_type or "application/octet-stream"

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(content)
            tmp_path = Path(tmp.name)

        try:
            raw_docs = load_documents_from_path(tmp_path, content_type=content_type)
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self._settings.chunk_size,
                chunk_overlap=self._settings.chunk_overlap,
            )
            chunks = splitter.split_documents(raw_docs)
            if not chunks:
                raise Error.bad_request("No text chunks produced from document")

            document = await self._document_repo.create_document(
                filename=file.filename,
                content_type=content_type,
                size_bytes=len(content),
                chunk_count=len(chunks),
            )

            try:
                self._vectorstore_service.add_chunks(
                    document_id=document.id,
                    filename=file.filename,
                    chunks=chunks,
                )
            except Exception:
                await self._document_repo.soft_delete(document.id)
                await self._vectorstore_service.delete_by_document_id(document.id)
                raise

            logger.info(
                f"{self._tag}|ingest_upload(): {file.filename} -> {len(chunks)} chunks"
            )
            return UploadResponse(
                document_id=document.id,
                filename=file.filename,
                chunk_count=len(chunks),
            )
        finally:
            tmp_path.unlink(missing_ok=True)
