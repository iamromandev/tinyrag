from tortoise.fields.base import StrEnum


class LlmProvider(StrEnum):
    OPENAI = "openai"
    OLLAMA = "ollama"
