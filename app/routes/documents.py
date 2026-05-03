from fastapi import APIRouter
from fastapi import Query
from datetime import datetime
from fastapi import HTTPException
from fastapi import Depends
from app.db.connection import get_db_connection
from app.models.documents import DocumentCreate, DocumentResponse


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
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[DocumentResponse])
def get_documents(
    author : str = Query(None),
    content_type: str = Query(None),
    conn = Depends(get_db_connection)):

    query = "SELECT id, title ,content, author, content, word_count FROM documents"
    params = []
    conditions = []
    if author:
        conditions.append("author = %s")
        params.append(author)
        
    if content_type:
        conditions.append('content_type = %s')
        params.append(content_type)

    if conditions:
        query += "WHERE" + 'AND'.join(conditions)
        query = query + "WHERE content_type = %s", (content_type)
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
            }
            for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code = 500, details = str(e))
            


@router.get('/{id}', response_model = DocumentResponse)
def get_document_by_id(id: int, conn = Depends(get_db_connection)):
    with conn.cursor() as cur:
        cur.execute("SELECT id, title, content, author, content_type, word_count FROM documents WHERE id = %s", (id,))
        result= cur.fetchone()
        return DocumentResponse(
            id=id,
            title=result.title,
            author=result.author,
            content_type=result.content_type,
            content=result.content,
            word_count=result.word_count,
            created_at=result[1]
        )


# @router.post("/")
# def create_document(request: Document, conn = Depends(get_db_connection)): 
#     try:
#         with conn.cursor() as cur:
#             cur.execute(
#             "INSERT INTO documents (title, content, author, content_type, word_count) VALUES (%s, %s, %s, %s, %s)",
#             (request.title, request.content, request.author, request.content_type, request.word_count)
#             )
#             conn.commit()
#         return {"message": "Document created"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/")
# def get_documents(conn = Depends(get_db_connection)): 
#     try:
#         with conn.cursor() as cur:
#             cur.execute("SELECT id, title, content, author, content_type, word_count FROM documents")
#             rows = cur.fetchall()
#             documents = [Document(id=row[0], title=row[1], content=row[2], author=row[3], content_type=row[4], word_count=row[5]) for row in rows]   
        
#         return documents
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/{id}")

# def get_document(id: int, conn = Depends(get_db_connection)):   
#     try: 
#         with conn.cursor() as cur:
#             cur.execute("SELECT id, title, content, author, content_type, word_count FROM documents WHERE id = %s", (id,))
#             row = cur.fetchone()
#             if row:
#                 document = Document(id=row[0], title=row[1], content=row[2], author=row[3], content_type=row[4], word_count=row[5])    
#                 return document
#             else:
#                 raise HTTPException(status_code=404, detail="Document not found")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}")
def delete_document(id: int, conn = Depends(get_db_connection)):
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE documents SET deleted_at = %d WHERE id = %s", (id, datetime.utcnow))
            conn.commit()    
        
        return {"message": f"Document {id} deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

