from fastapi import APIRouter

from .crud import router as _crud_router

_subrouters = [_crud_router]

router = APIRouter(prefix="/prompt", tags=["Prompt"])

for subrouter in _subrouters:
    router.include_router(subrouter)
