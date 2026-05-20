from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from src.config import Settings, get_settings
from src.core.common import serialize
from src.core.error import Error
from src.data.type import LlmProvider


def get_embeddings(settings: Settings | None = None) -> Embeddings:
    settings = settings or get_settings()
    provider = settings.effective_embedding_provider

    if provider == LlmProvider.OPENAI:
        api_key = settings.openai_api_key
        key_value = serialize(api_key) if api_key is not None else ""
        if not key_value.strip():
            raise Error.bad_request("OPENAI_API_KEY is required for OpenAI embeddings")
        return OpenAIEmbeddings(
            api_key=key_value,
            model=settings.openai_embedding_model,
        )

    return OllamaEmbeddings(
        base_url=settings.ollama_base_url,
        model=settings.ollama_embedding_model,
    )


def get_chat_model(settings: Settings | None = None) -> BaseChatModel:
    settings = settings or get_settings()
    provider = settings.llm_provider

    if provider == LlmProvider.OPENAI:
        api_key = settings.openai_api_key
        key_value = serialize(api_key) if api_key is not None else ""
        if not key_value.strip():
            raise Error.bad_request("OPENAI_API_KEY is required for OpenAI chat")
        return ChatOpenAI(
            api_key=key_value,
            model=settings.openai_chat_model,
        )

    return ChatOllama(
        base_url=settings.ollama_base_url,
        model=settings.ollama_chat_model,
    )
