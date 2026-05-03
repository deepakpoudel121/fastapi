from fastapi import APIRouter
from fastapi import Query
from datetime import datetime
from fastapi import HTTPException
from fastapi import Depends
from app.db.connection import get_db_connection
from app.models.documents import DocumentCreate, DocumentResponse
from app.core.logger import logger


router = APIRouter(prefix="/documents")


@router.post("/", response_model=DocumentResponse)
def create_document(request: DocumentCreate, conn = Depends(get_db_connection)):
    try:
        with conn.cursor() as cur:
            cur.execute(
            "INSERT INTO documents (title, content, author, content_type, word_count) VALUES (%s, %s, %s, %s, %s) RETURNING id, created_at",
            (request.title, request.content, request.author, request.content_type, request.word_count)
            )
            result = cur.fetchone()
            conn.commit()
        
        return DocumentResponse(
            id=result[0],
            title=request.title,
            author=request.author,
            content_type=request.content_type,
            content=request.content,
            word_count=request.word_count,
            created_at=result[1]
        )
    except Exception as e:
        logger.error("failed to create document", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=list[DocumentResponse])
def get_documents(
    author: str = Query(None),
    content_type: str = Query(None),
    conn=Depends(get_db_connection)
):
    query = """
    SELECT id, title, content, author, content_type, word_count, created_at
    FROM documents
    WHERE deleted_at IS NULL
    """

    params = []
    conditions = []

    if author:
        conditions.append("author = %s")
        params.append(author)

    if content_type:
        conditions.append("content_type = %s")
        params.append(content_type)

    if conditions:
        query += " AND " + " AND ".join(conditions)

    try:
        with conn.cursor() as cur:
            cur.execute(query, tuple(params))
            rows = cur.fetchall()

        return [
            {
                "id": row[0],
                "title": row[1],
                "content": row[2],
                "author": row[3],
                "content_type": row[4],
                "word_count": row[5],
                # optionally include created_at
                "created_at": row[6],
            }
            for row in rows
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
            


@router.get('/{id}', response_model = DocumentResponse)
def get_document_by_id(id: int, conn = Depends(get_db_connection)):
    try: 
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, content, author, content_type, word_count, created_at FROM documents WHERE id = %s AND deleted_at IS NULL" , (id,))
            row= cur.fetchone()
    except Exception as e:
            raise HTTPException(status_code = 500, detail = str(e))
    if not row:
            raise HTTPException(status_code = 404, detail= "Not Found")
            
    return DocumentResponse(
        id= row[0],
        title  = row[1],
        content = row[2],
        author = row[3],
        content_type =row[4],
        word_count = row[5],
        created_at = row[6]
    )
       
    
    

@router.delete('/{id}')
def delete_document(id: int, conn = Depends(get_db_connection)):
    try:
        with conn.cursor() as cur:
            cur.execute('UPDATE documents SET deleted_at = NOW() WHERE id = %s AND deleted_at IS NULL RETURNING id', (id,))
            row = cur.fetchone()
            conn.commit()
    except Exception as e:
            raise HTTPException(status_code = 500, detail = str(e))
    if not row:
            raise HTTPException(status_code = 404, detail= "Not Found")
    return {f"Message": f"Document with id {id} deleted successfully"}
    
