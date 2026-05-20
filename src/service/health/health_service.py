import httpx
from loguru import logger

from src.config import get_settings
from src.core.base import BaseService
from src.core.common import get_app_version
from src.core.type import Status
from src.data.db import get_db_health, get_db_version
from src.data.schema.health import DatabaseSchema, HealthSchema, LlmSchema
from src.data.type import LlmProvider


class HealthService(BaseService):
    async def check_health(self) -> HealthSchema:
        settings = get_settings()
        db_status = Status.SUCCESS if await get_db_health() else Status.ERROR
        db_version = await get_db_version()

        llm_status = Status.SUCCESS
        if settings.llm_provider == LlmProvider.OLLAMA:
            try:
                async with httpx.AsyncClient(timeout=3.0) as client:
                    response = await client.get(f"{settings.ollama_base_url.rstrip('/')}/api/tags")
                    if response.status_code >= 400:
                        llm_status = Status.ERROR
            except Exception as error:
                logger.warning(f"{self._tag}|check_health(): ollama unreachable: {error}")
                llm_status = Status.ERROR

        return HealthSchema(
            version=get_app_version(),
            db=DatabaseSchema(status=db_status, version=db_version),
            llm=LlmSchema(
                status=llm_status,
                provider=str(settings.llm_provider),
            ),
        )
