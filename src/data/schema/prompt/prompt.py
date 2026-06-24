import uuid
from datetime import datetime
from typing import Annotated, Any

from pydantic import Field

from src.core.base import BaseSchema


class PromptVersionSchema(BaseSchema):
    id: uuid.UUID
    version: int
    config: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class PromptSchema(BaseSchema):
    id: uuid.UUID
    key: str
    name: str
    description: str | None = None
    is_active: bool
    created_at: datetime
    versions: list[PromptVersionSchema] | None = None


class CreatePromptRequest(BaseSchema):
    key: Annotated[str, Field(min_length=1, max_length=128)]
    name: Annotated[str, Field(min_length=1, max_length=255)]
    description: str | None = None
    config: dict[str, Any] = Field(default_factory=dict)


class UpdatePromptRequest(BaseSchema):
    name: Annotated[str | None, Field(default=None, min_length=1, max_length=255)] = None
    description: str | None = None
    is_active: bool | None = None


class AddVersionRequest(BaseSchema):
    config: dict[str, Any] = Field(default_factory=dict)
