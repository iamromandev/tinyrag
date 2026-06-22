from fastapi import APIRouter

from .crud import router as _crud_router
from .upload import router as _upload_router

_subrouters = [_upload_router, _crud_router]

router = APIRouter(prefix="/document", tags=["Document"])

for subrouter in _subrouters:
    router.include_router(subrouter)
