from __future__ import annotations

import uuid

from loguru import logger

from src.core.base import BaseService
from src.core.error import Error
from src.data.db.model import Prompt
from src.data.repo.interface.prompt import PromptRepo
from src.data.schema.prompt import (
    AddVersionRequest,
    CreatePromptRequest,
    PromptSchema,
    PromptVersionSchema,
    UpdatePromptRequest,
)


class PromptService(BaseService):
    def __init__(self, prompt_repo: PromptRepo) -> None:
        super().__init__()
        self._prompt_repo = prompt_repo

    async def _to_schema(
        self, prompt: Prompt, *, include_versions: bool = False
    ) -> PromptSchema:
        versions = None
        if include_versions:
            rows = await self._prompt_repo.list_versions(prompt.id)
            versions = [PromptVersionSchema.model_validate(v) for v in rows]
        return PromptSchema(
            id=prompt.id,
            key=prompt.key,
            name=prompt.name,
            description=prompt.description,
            is_active=prompt.is_active,
            created_at=prompt.created_at,
            versions=versions,
        )

    async def create_prompt(self, request: CreatePromptRequest) -> PromptSchema:
        existing = await self._prompt_repo.get_by_key_active(request.key)
        if existing is not None:
            raise Error.conflict(f"Prompt with key '{request.key}' already exists")

        prompt = await self._prompt_repo.create_prompt(
            key=request.key,
            name=request.name,
            description=request.description,
            config=request.config,
        )
        logger.info(f"{self._tag}|create_prompt(): created {prompt.id} ({prompt.key})")
        return await self._to_schema(prompt, include_versions=True)

    async def list_prompts(self) -> list[PromptSchema]:
        rows = await self._prompt_repo.list_active()
        return [await self._to_schema(row) for row in rows]

    async def get_prompt(self, prompt_id: uuid.UUID) -> PromptSchema:
        prompt = await self._prompt_repo.get_by_id_active(prompt_id)
        if prompt is None:
            raise Error.not_found(f"Prompt {prompt_id} not found")
        return await self._to_schema(prompt, include_versions=True)

    async def update_prompt(
        self, prompt_id: uuid.UUID, request: UpdatePromptRequest
    ) -> PromptSchema:
        fields = request.to_dict(exclude_none=True, exclude_unset=True)
        # is_active is derived from deleted_at, not a stored column. Setting it
        # to False is a soft-delete; True is a no-op (active prompts are already
        # active, and deactivated ones are hidden from active queries).
        is_active = fields.pop("is_active", None)
        # Apply name/description while the prompt is still active. is_active=True
        # is a no-op; is_active=False deactivates via soft-delete (deactivation
        # and deletion converge on deleted_at).
        prompt = await self._prompt_repo.update_prompt(prompt_id, **fields)
        if prompt is None:
            raise Error.not_found(f"Prompt {prompt_id} not found")
        if is_active is False:
            await self._prompt_repo.soft_delete(prompt_id)
            await prompt.refresh_from_db(fields=["deleted_at"])
            logger.info(f"{self._tag}|update_prompt(): deactivated {prompt_id}")
        return await self._to_schema(prompt, include_versions=True)

    async def delete_prompt(self, prompt_id: uuid.UUID) -> None:
        deleted = await self._prompt_repo.soft_delete(prompt_id)
        if not deleted:
            raise Error.not_found(f"Prompt {prompt_id} not found")
        logger.info(f"{self._tag}|delete_prompt(): deleted {prompt_id}")

    async def add_version(
        self, prompt_id: uuid.UUID, request: AddVersionRequest
    ) -> PromptSchema:
        prompt = await self._prompt_repo.get_by_id_active(prompt_id)
        if prompt is None:
            raise Error.not_found(f"Prompt {prompt_id} not found")
        await self._prompt_repo.add_version(
            prompt_id,
            config=request.config,
        )
        prompt = await self._prompt_repo.get_by_id_active(prompt_id)
        assert prompt is not None
        return await self._to_schema(prompt, include_versions=True)

    async def list_versions(self, prompt_id: uuid.UUID) -> list[PromptVersionSchema]:
        prompt = await self._prompt_repo.get_by_id_active(prompt_id)
        if prompt is None:
            raise Error.not_found(f"Prompt {prompt_id} not found")
        rows = await self._prompt_repo.list_versions(prompt_id)
        return [PromptVersionSchema.model_validate(v) for v in rows]
