from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.core.success import Success
from src.data.schema.chat import ChatRequest, ChatResponse
from src.service import RagService, get_rag_service

router = APIRouter()


@router.post(
    path="/",
    response_model=Success[ChatResponse],
)
async def chat(
    body: ChatRequest,
    rag_service: Annotated[RagService, Depends(get_rag_service)],
) -> JSONResponse:
    data = await rag_service.chat(body)
    return Success.ok(data=data).to_resp()
