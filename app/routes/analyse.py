import time
from fastapi import APIRouter, Query, Depends, HTTPException
from app.db.connection import get_db_connection
from app.llm import LLMResponse, get_llm_chain
from app.core import logger
from rich import print
router = APIRouter(prefix='/analyse')


def get_chain_with_fallback(primary:str):
    fallback_order = {
        'mistral': ['mistral', 'groq'],
        'groq': ['groq', 'mistral']
    }
    providers = fallback_order.get(primary, ['mistral', 'groq'])
    for provider in providers:
        try:
            return get_llm_chain(provider), provider
        except Exception as e:
            last_error = e
            continue
    raise last_error

@router.post('/', response_model=LLMResponse)
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
        chain, model_used= get_chain_with_fallback(provider)
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
        model_used=model_used,
        latency_ms=latency_ms,
        cost_usd=0.0
    )