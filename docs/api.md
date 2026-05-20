# TinyRAG API

## Dev workflow

```bash
cp .env.example .env
make install
make up
make migrate
make run
```

OpenAPI: http://localhost:8000/docs

### Ollama (local LLM)

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

Set `LLM_PROVIDER=ollama` and `EMBEDDING_PROVIDER=ollama` in `.env`.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health/check` | App, database, and LLM provider health |
| POST | `/documents/upload` | Upload PDF, DOCX, TXT, or MD; chunk and embed |
| GET | `/documents` | List uploaded documents |
| DELETE | `/documents/{document_id}` | Soft-delete document and remove vectors |
| POST | `/chat` | RAG chat over uploaded documents |

### Chat request

```json
{
  "message": "What is this document about?",
  "document_ids": ["optional-uuid-to-filter"]
}
```

### Chat response (inside Success envelope)

```json
{
  "answer": "...",
  "sources": [
    {
      "document_id": "...",
      "filename": "report.pdf",
      "chunk_index": 0,
      "snippet": "..."
    }
  ]
}
```
