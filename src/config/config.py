from functools import lru_cache
from typing import Annotated
from urllib.parse import quote_plus

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.common import serialize
from src.data.type import Env

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    env: Annotated[Env, Field(description="Application environment")]
    debug: Annotated[bool, Field(description="Enable debug mode")]

    db_schema: Annotated[str, Field(description="Database schema label")]
    db_host: Annotated[str, Field(description="Database host")]
    db_port: Annotated[int, Field(description="Database port")]
    db_name: Annotated[str, Field(description="Database name")]
    db_user: Annotated[str, Field(description="Database user")]
    db_password: Annotated[SecretStr, Field(description="Database password")]

    openrouter_api_key: Annotated[SecretStr | None, Field(default=None, description="OpenRouter API key")] = None
    openrouter_base_url: Annotated[str, Field(description="OpenRouter API base URL")] = "https://openrouter.ai/api/v1"
    openrouter_chat_model: str = "openai/gpt-4o-mini"
    openrouter_embedding_model: str = "nvidia/llama-nemotron-embed-vl-1b-v2:free"

    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_top_k: int = 4
    collection_name: str = "tinyrag"
    max_upload_bytes: int = 20 * 1024 * 1024

    cors_origins: str = ""

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
