from fastapi import APIRouter

from .chat import router as _chat_router
from .document import router as _documents_router
from .health import router as _health_router
from .prompt import router as _prompt_router

_subrouters = [
    _health_router,
    _documents_router,
    _prompt_router,
    _chat_router,
]

router = APIRouter()

for subrouter in _subrouters:
    router.include_router(subrouter)
