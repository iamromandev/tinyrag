from fastapi import APIRouter

from .chat import router as _chat_router
from .documents import router as _documents_router
from .health import router as _health_router

_subrouters = [
    _health_router,
    _documents_router,
    _chat_router,
]

router = APIRouter()

for subrouter in _subrouters:
    router.include_router(subrouter)
