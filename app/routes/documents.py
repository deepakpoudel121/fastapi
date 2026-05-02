from fastapi import APIRouter

router = APIRouter(prefix="/documents")

@router.post("/")
async def create_document():    return {"message": "Document created"}

@router.get("/")
async def get_documents():    return {"message": "List of documents"}

@router.get("/{id}")
async def get_document(id: int):    return {"message": f"Document {id}"}


@router.delete("/{id}")
async def delete_document(id: int):    return {"message": f"Document {id} deleted"}

