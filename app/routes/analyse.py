import time
from fastapi import APIRouter, Query, Depends, HTTPException
from app.db.connection import get_db_connection
from app.llm import LLMResponse, get_llm_chain
from app.core import logger
from rich import print
router = APIRouter(prefix='/analyse')

@router.get('/', response_model=LLMResponse)
def analyse_document(
    db=Depends(get_db_connection),
    provider: str = Query(default="mistral"),
    id: int = Query()
):
    # 1. Fetch document
    with db.cursor() as cur:
        cur.execute(
            'SELECT content FROM documents WHERE id = %s AND deleted_at IS NULL',
            (id,)
        )
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Document not found")

    # 2. Call LLM with latency tracking
    try:
        start = time.time()
        chain = get_llm_chain(provider)
        print(chain)
        response = chain.invoke({"document": row[0]})
        print(response)
        latency_ms = round((time.time() - start) * 1000)
    except Exception as e:
        logger.error("LLM call failed", extra={"error": str(e)})
        raise HTTPException(status_code=502, detail="LLM service unavailable")

    # 3. Build and return response
    return LLMResponse(
        document_id=id,
        summary=response.summary,
        key_topics=response.key_topics,
        sentiment=response.sentiment,
        suggested_tags=response.suggested_tags,
        model_used=provider,
        latency_ms=latency_ms,
        cost_usd=0.0
    )