from src.config import get_settings
from src.core.base import BaseService
from src.core.common import get_app_version
from src.core.type import Status
from src.data.db import get_db_health, get_db_version
from src.data.schema.health import DatabaseSchema, HealthSchema, LlmSchema
from src.data.type import LlmProvider
from src.lib.llm_factory import get_llm_health


class HealthService(BaseService):
    async def check_health(self) -> HealthSchema:
        settings = get_settings()
        db_status = Status.SUCCESS if await get_db_health() else Status.ERROR
        db_version = await get_db_version()
        llm_status = Status.SUCCESS if await get_llm_health(settings) else Status.ERROR

        return HealthSchema(
            version=get_app_version(),
            db=DatabaseSchema(status=db_status, version=db_version),
            llm=LlmSchema(
                status=llm_status,
                provider=LlmProvider.OPENROUTER,
            ),
        )
