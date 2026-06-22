from pathlib import Path

from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader
from langchain_core.documents import Document as LcDocument

from src.core.error import Error

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}


def load_documents_from_path(path: Path,   content_type: str) -> list[LcDocument]:
    suffix = path.suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise Error.bad_request(
            f"Unsupported file type '{suffix}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    if suffix == ".pdf":
        loader = PyPDFLoader(str(path))
    elif suffix == ".docx":
        loader = Docx2txtLoader(str(path))
    else:
        loader = TextLoader(str(path), encoding="utf-8")

    docs = loader.load()
    if not docs:
        raise Error.bad_request("Document contains no extractable text")

    for doc in docs:
        doc.metadata.setdefault("content_type", content_type)

    return docs
