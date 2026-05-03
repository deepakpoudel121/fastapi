# Document Metadata Service

A REST API for storing and querying document metadata, built with FastAPI and PostgreSQL.

## Stack
FastAPI · PostgreSQL · psycopg2 · Docker · Python 3.13

## Endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | /documents/ | Create a document |
| GET | /documents/ | List documents (filter by author, content_type) |
| GET | /documents/{id} | Get document by ID |
| DELETE | /documents/{id} | Soft delete a document |
| GET | /health | DB health check |

## Run locally
\```bash
# 1. Clone and install
uv sync

# 2. Set up environment
cp .env.example .env
# fill in your DB credentials

# 3. Run migration
psql -U postgres -d docservice < app/db/migrations/001_create_documents.sql

# 4. Start server
uv run uvicorn app.main:app --reload
\```

## Example
\```bash
curl -X POST http://localhost:8000/documents/ \
  -H "Content-Type: application/json" \
  -d '{"title":"My Doc","author":"Alice","content_type":"pdf","content":"Hello","word_count":1}'
\```