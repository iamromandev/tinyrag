import uuid
from datetime import datetime

from src.core.base import BaseSchema


class DocumentSchema(BaseSchema):
    id: uuid.UUID
    filename: str
    content_type: str
    size_bytes: int
    chunk_count: int
    created_at: datetime


class UploadResponse(BaseSchema):
    document_id: uuid.UUID
    filename: str
    chunk_count: int
