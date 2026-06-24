from collections.abc import AsyncGenerator

from .document_db import DocumentDatabaseRepo
from .prompt_db import PromptDatabaseRepo


async def get_document_database_repo() -> AsyncGenerator[DocumentDatabaseRepo]:
    yield DocumentDatabaseRepo()


async def get_prompt_database_repo() -> AsyncGenerator[PromptDatabaseRepo]:
    yield PromptDatabaseRepo()
