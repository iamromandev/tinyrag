from __future__ import annotations

import uuid
from typing import Any

from src.core.base import BaseRepo
from src.data.db.model import Prompt, PromptVersion
from src.data.repo.interface.prompt import PromptRepo


class PromptDatabaseRepo(BaseRepo[Prompt], PromptRepo):
    def __init__(self) -> None:
        super().__init__(Prompt)

    async def create_prompt(
        self,
        *,
        key: str,
        name: str,
        description: str | None = None,
        config: dict[str, Any] | None = None,
    ) -> Prompt:
        prompt = await self.create(
            key=key,
            name=name,
            description=description,
        )
        await PromptVersion.create(
            prompt=prompt,
            version=1,
            config=config or {},
        )
        return prompt

    async def get_by_id_active(self, prompt_id: uuid.UUID) -> Prompt | None:
        return await self.get_one(id=prompt_id, deleted_at__isnull=True)

    async def get_by_key_active(self, key: str) -> Prompt | None:
        return await self.get_one(key=key, deleted_at__isnull=True)

    async def list_active(self) -> list[Prompt]:
        return await Prompt.get_active().order_by("-created_at")

    async def add_version(
        self,
        prompt_id: uuid.UUID,
        *,
        config: dict[str, Any] | None = None,
    ) -> PromptVersion:
        prompt = await self.get_by_id_active(prompt_id)
        if prompt is None:
            msg = f"Prompt {prompt_id} not found"
            raise ValueError(msg)
        latest = (
            await PromptVersion.filter(prompt_id=prompt_id).order_by("-version").first()
        )
        next_version = (latest.version if latest else 0) + 1
        return await PromptVersion.create(
            prompt_id=prompt_id,
            version=next_version,
            config=config or {},
        )

    async def get_version(
        self, prompt_id: uuid.UUID, version: int
    ) -> PromptVersion | None:
        return await PromptVersion.filter(
            prompt_id=prompt_id, version=version
        ).first()

    async def list_versions(self, prompt_id: uuid.UUID) -> list[PromptVersion]:
        return await PromptVersion.filter(prompt_id=prompt_id).order_by("-version")

    async def update_prompt(
        self, prompt_id: uuid.UUID, **fields: object
    ) -> Prompt | None:
        prompt = await self.get_by_id_active(prompt_id)
        if prompt is None:
            return None
        return await self.update(prompt, **fields)

    async def soft_delete(self, prompt_id: uuid.UUID) -> bool:
        prompt = await self.get_by_id_active(prompt_id)
        if prompt is None:
            return False
        await prompt.soft_delete()
        return True
