from __future__ import annotations

import uuid

from langchain_core.documents import Document as LcDocument
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from src.config import Settings, get_settings
from src.core.base import BaseService
from src.data.schema.chat import ChatRequest, ChatResponse, SourceSchema
from src.lib.llm_factory import get_chat_model
from src.service.vectorstore_service import VectorstoreService

SYSTEM_PROMPT = (
    "Answer the question using only the context below. "
    "If the answer is not in the context, say you do not know.\n\n"
    "Context:\n{context}"
)


def _format_docs(docs: list[LcDocument]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


class RagService(BaseService):
    def __init__(
        self,
        vectorstore_service: VectorstoreService,
        settings: Settings | None = None,
    ) -> None:
        super().__init__()
        self._vectorstore_service = vectorstore_service
        self._settings = settings or get_settings()

    async def chat(self, request: ChatRequest) -> ChatResponse:
        retriever = self._vectorstore_service.as_retriever(
            document_ids=request.document_ids,
        )
        docs = await retriever.ainvoke(request.message)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                ("human", "{question}"),
            ]
        )
        chain = (
            {
                "context": lambda _: _format_docs(docs),
                "question": RunnablePassthrough(),
            }
            | prompt
            | get_chat_model(self._settings)
            | StrOutputParser()
        )
        answer = await chain.ainvoke(request.message)

        sources: list[SourceSchema] = []
        for doc in docs:
            meta = doc.metadata
            doc_id_raw = meta.get("document_id")
            if not doc_id_raw:
                continue
            sources.append(
                SourceSchema(
                    document_id=uuid.UUID(str(doc_id_raw)),
                    filename=str(meta.get("filename", "")),
                    chunk_index=int(meta.get("chunk_index", 0)),
                    snippet=doc.page_content[:500],
                )
            )

        return ChatResponse(answer=answer, sources=sources)
