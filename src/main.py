from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.core.common import get_app_version
from src.core.error import init_global_errors
from src.data.db import init_db
from src.route import router as _router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="TinyRAG",
        description="Document upload and RAG chat with LangChain and pgvector.",
        version=get_app_version(),
        debug=settings.debug,
        lifespan=lifespan,
    )
    if settings.cors_origin_list:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origin_list,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    init_global_errors(app)

    for router in [_router]:
        app.include_router(router)

    init_db(app)
    return app


app = create_app()


def run() -> None:
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        loop="uvloop",
    )
