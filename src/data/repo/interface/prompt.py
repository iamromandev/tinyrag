from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import Any

from src.data.db.model import Prompt, PromptVersion


class PromptRepo(ABC):
    @abstractmethod
    async def create_prompt(
        self,
        *,
        key: str,
        name: str,
        description: str | None = None,
        config: dict[str, Any] | None = None,
    ) -> Prompt:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id_active(self, prompt_id: uuid.UUID) -> Prompt | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_key_active(self, key: str) -> Prompt | None:
        raise NotImplementedError

    @abstractmethod
    async def list_active(self) -> list[Prompt]:
        raise NotImplementedError

    @abstractmethod
    async def add_version(
        self,
        prompt_id: uuid.UUID,
        *,
        config: dict[str, Any] | None = None,
    ) -> PromptVersion:
        raise NotImplementedError

    @abstractmethod
    async def get_version(
        self, prompt_id: uuid.UUID, version: int
    ) -> PromptVersion | None:
        raise NotImplementedError

    @abstractmethod
    async def list_versions(self, prompt_id: uuid.UUID) -> list[PromptVersion]:
        raise NotImplementedError

    @abstractmethod
    async def update_prompt(self, prompt_id: uuid.UUID, **fields: object) -> Prompt | None:
        raise NotImplementedError

    @abstractmethod
    async def soft_delete(self, prompt_id: uuid.UUID) -> bool:
        raise NotImplementedError
