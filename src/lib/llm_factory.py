import httpx
from langchain.chat_models import init_chat_model
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import OpenAIEmbeddings
from loguru import logger
from pydantic import SecretStr

from src.config import Settings, get_settings
from src.core.common import serialize
from src.core.error import Error


def _require_api_key(settings: Settings) -> str:
    api_key = settings.openrouter_api_key
    key_value = serialize(api_key) if api_key is not None else ""
    if not key_value.strip():
        raise Error.bad_request("OPENROUTER_API_KEY is required")
    return key_value


def get_embeddings(settings: Settings | None = None) -> Embeddings:
    settings = settings or get_settings()
    return OpenAIEmbeddings(
        api_key=SecretStr(_require_api_key(settings)),
        base_url=settings.openrouter_base_url,
        model=settings.openrouter_embedding_model,
        check_embedding_ctx_length=False,
    )


def get_chat_model(settings: Settings | None = None) -> BaseChatModel:
    settings = settings or get_settings()
    return init_chat_model(
        f"openai:{settings.openrouter_chat_model}",
        api_key=_require_api_key(settings),
        base_url=settings.openrouter_base_url,
    )


async def get_llm_health(settings: Settings | None = None) -> bool:
    settings = settings or get_settings()
    try:
        api_key = _require_api_key(settings)
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{settings.openrouter_base_url.rstrip('/')}/key",
                headers={"Authorization": f"Bearer {api_key}"},
            )
        response.raise_for_status()
        logger.error("Success|get_llm_health(): {}", response.json())
        return True
    except Exception as error:
        logger.error("Error|get_llm_health(): {}", error)
        return False
