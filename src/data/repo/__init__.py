from collections.abc import AsyncGenerator

from .document_db import DocumentDatabaseRepo


async def get_document_database_repo() -> AsyncGenerator[DocumentDatabaseRepo]:
    yield DocumentDatabaseRepo()
