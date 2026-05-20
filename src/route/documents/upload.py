from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse

from src.core.success import Success
from src.data.schema.document import UploadResponse
from src.service import IngestionService, get_ingestion_service

router = APIRouter()


@router.post(
    path="/upload",
    response_model=Success[UploadResponse],
)
async def upload_document(
    file: Annotated[UploadFile, File()],
    ingestion_service: Annotated[IngestionService, Depends(get_ingestion_service)],
) -> JSONResponse:
    data = await ingestion_service.ingest_upload(file)
    return Success.created(data=data).to_resp()
