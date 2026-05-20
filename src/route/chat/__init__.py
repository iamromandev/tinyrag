from fastapi import APIRouter

from .chat import router as _chat_router

_subrouters = [_chat_router]

router = APIRouter(prefix="/chat", tags=["Chat"])

for subrouter in _subrouters:
    router.include_router(subrouter)
