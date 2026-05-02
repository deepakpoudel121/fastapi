from fastapi import APIRouter
from fastapi import Depends
from app.db.connection import get_db_connection
from app.models.documents import Document
router = APIRouter(prefix="/documents")



@router.post("/")
def create_document(request: Document, conn = Depends(get_db_connection)): 
    with conn.cursor() as cur:
        cur.execute(
        "INSERT INTO documents (title, content, author, content_type, word_count) VALUES (%s, %s, %s, %s, %s)",
        (request.title, request.content, request.author, request.content_type, request.word_count)
        )
        conn.commit()
    return {"message": "Document created"}

@router.get("/")
async def get_documents(conn = Depends(get_db_connection)): 
    with conn.cursor() as cur:
        cur.execute("SELECT id, title, content, author, content_type, word_count FROM documents")
        rows = cur.fetchall()
        documents = [Document(id=row[0], title=row[1], content=row[2], author=row[3], content_type=row[4], word_count=row[5]) for row in rows]   
    
    return documents

@router.get("/{id}")
async def get_document(id: int, conn = Depends(get_db_connection)):    
    with conn.cursor() as cur:
        cur.execute("SELECT id, title, content, author, content_type, word_count FROM documents WHERE id = %s", (id,))
        row = cur.fetchone()
        if row:
            document = Document(id=row[0], title=row[1], content=row[2], author=row[3], content_type=row[4], word_count=row[5])    
            return document
        else:
            return {"message": "Document not found"}


@router.delete("/{id}")
async def delete_document(id: int, conn = Depends(get_db_connection)):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM documents WHERE id = %s", (id,))
        conn.commit()    
    
    return {"message": f"Document {id} deleted"}

