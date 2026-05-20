from typing import Annotated

from pydantic import Field

from src.core.base import BaseSchema
from src.core.type import Status


class DatabaseSchema(BaseSchema):
    status: Annotated[Status, Field(default=Status.ERROR)]
    version: Annotated[str | None, Field(default=None)]


class LlmSchema(BaseSchema):
    status: Annotated[Status, Field(default=Status.ERROR)]
    provider: Annotated[str | None, Field(default=None)]


class HealthSchema(BaseSchema):
    version: Annotated[str, Field(default="0.0.1")] = "0.0.1"
    db: Annotated[DatabaseSchema | None, Field(default=None)] = None
    llm: Annotated[LlmSchema | None, Field(default=None)] = None
