import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.core.success import Success
from src.data.schema.document import DocumentSchema
from src.service import DocumentService, get_document_service

router = APIRouter()


@router.get(
    path="/",
    response_model=Success[list[DocumentSchema]],
)
async def list_documents(
    document_service: Annotated[DocumentService, Depends(get_document_service)],
) -> JSONResponse:
    data = await document_service.list_documents()
    return Success.ok(data=data).to_resp()


@router.delete(
    path="/{document_id}",
    response_model=Success[None],
)
async def delete_document(
    document_id: uuid.UUID,
    document_service: Annotated[DocumentService, Depends(get_document_service)],
) -> JSONResponse:
    await document_service.delete_document(document_id)
    return Success.no_content(message="Document deleted").to_resp()
