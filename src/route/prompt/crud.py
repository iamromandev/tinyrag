import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.core.success import Success
from src.data.schema.prompt import (
    AddVersionRequest,
    CreatePromptRequest,
    PromptSchema,
    PromptVersionSchema,
    UpdatePromptRequest,
)
from src.service import PromptService, get_prompt_service

router = APIRouter()


@router.post(
    path="/",
    response_model=Success[PromptSchema],
)
async def create_prompt(
    request: CreatePromptRequest,
    prompt_service: Annotated[PromptService, Depends(get_prompt_service)],
) -> JSONResponse:
    data = await prompt_service.create_prompt(request)
    return Success.created(data=data, message="Prompt created").to_resp()


@router.get(
    path="/",
    response_model=Success[list[PromptSchema]],
)
async def list_prompts(
    prompt_service: Annotated[PromptService, Depends(get_prompt_service)],
) -> JSONResponse:
    data = await prompt_service.list_prompts()
    return Success.ok(data=data).to_resp()


@router.get(
    path="/{prompt_id}",
    response_model=Success[PromptSchema],
)
async def get_prompt(
    prompt_id: uuid.UUID,
    prompt_service: Annotated[PromptService, Depends(get_prompt_service)],
) -> JSONResponse:
    data = await prompt_service.get_prompt(prompt_id)
    return Success.ok(data=data).to_resp()


@router.patch(
    path="/{prompt_id}",
    response_model=Success[PromptSchema],
)
async def update_prompt(
    prompt_id: uuid.UUID,
    request: UpdatePromptRequest,
    prompt_service: Annotated[PromptService, Depends(get_prompt_service)],
) -> JSONResponse:
    data = await prompt_service.update_prompt(prompt_id, request)
    return Success.ok(data=data, message="Prompt updated").to_resp()


@router.delete(
    path="/{prompt_id}",
    response_model=Success[None],
)
async def delete_prompt(
    prompt_id: uuid.UUID,
    prompt_service: Annotated[PromptService, Depends(get_prompt_service)],
) -> JSONResponse:
    await prompt_service.delete_prompt(prompt_id)
    return Success.no_content(message="Prompt deleted").to_resp()


@router.get(
    path="/{prompt_id}/versions",
    response_model=Success[list[PromptVersionSchema]],
)
async def list_versions(
    prompt_id: uuid.UUID,
    prompt_service: Annotated[PromptService, Depends(get_prompt_service)],
) -> JSONResponse:
    data = await prompt_service.list_versions(prompt_id)
    return Success.ok(data=data).to_resp()


@router.post(
    path="/{prompt_id}/versions",
    response_model=Success[PromptSchema],
)
async def add_version(
    prompt_id: uuid.UUID,
    request: AddVersionRequest,
    prompt_service: Annotated[PromptService, Depends(get_prompt_service)],
) -> JSONResponse:
    data = await prompt_service.add_version(prompt_id, request)
    return Success.created(data=data, message="Version added").to_resp()
