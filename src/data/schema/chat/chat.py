import uuid
from typing import Annotated

from pydantic import Field

from src.core.base import BaseSchema


class ChatRequest(BaseSchema):
    message: Annotated[str, Field(min_length=1)]
    document_ids: list[uuid.UUID] | None = None


class SourceSchema(BaseSchema):
    document_id: uuid.UUID
    filename: str
    chunk_index: int
    snippet: str


class ChatResponse(BaseSchema):
    answer: str
    sources: list[SourceSchema]
