from functools import lru_cache
from pathlib import Path
from typing import Annotated, Any
from urllib.parse import quote_plus

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.common import serialize
from src.data.type import Env, LlmProvider

_IN_DOCKER = Path("/.dockerenv").is_file()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=None if _IN_DOCKER else ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: Annotated[Env, Field(description="Application environment")]
    debug: Annotated[bool, Field(description="Enable debug mode")]

    db_schema: Annotated[str, Field(description="Database schema label")]
    db_host: Annotated[str, Field(description="Database host")]
    db_port: Annotated[int, Field(description="Database port")]
    db_name: Annotated[str, Field(description="Database name")]
    db_user: Annotated[str, Field(description="Database user")]
    db_password: Annotated[SecretStr, Field(description="Database password")]

    llm_provider: Annotated[LlmProvider, Field(description="Chat model provider")] = LlmProvider.OPENAI
    embedding_provider: Annotated[
        LlmProvider | None,
        Field(default=None, description="Embedding provider; defaults to llm_provider"),
    ] = None
    openai_api_key: Annotated[SecretStr | None, Field(default=None, description="OpenAI API key")] = None
    ollama_base_url: Annotated[str, Field(description="Ollama base URL")] = "http://localhost:11434"
    openai_chat_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    ollama_chat_model: str = "llama3.2"
    ollama_embedding_model: str = "nomic-embed-text"

    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_top_k: int = 4
    collection_name: str = "tinyrag"
    max_upload_bytes: int = 20 * 1024 * 1024

    cors_origins: str = ""

    @field_validator("embedding_provider", mode="before")
    @classmethod
    def empty_embedding_provider_is_none(cls, value: Any) -> Any:
        if value == "" or value is None:
            return None
        return value

    @property
    def effective_embedding_provider(self) -> LlmProvider:
        return self.embedding_provider or self.llm_provider

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def langchain_database_url(self) -> str:
        password = quote_plus(serialize(self.db_password))
        user = quote_plus(self.db_user)
        return (
            f"postgresql+psycopg://{user}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
