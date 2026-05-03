from app.routes import documents_router
from fastapi import FastAPI
from fastapi import Depends
from app.db.connection import get_db_connection 




app = FastAPI()

app.include_router(documents_router)


@app.get("/")
async def root():    return {"message": "Welcome to the Document Retrieval API"}

@app.get("/health")
async def health_check(db = Depends(get_db_connection)):
    with db.cursor() as cur:
        cur.execute("SELECT 1")
        result = cur.fetchone()
        if result and result[0] == 1:    
            return {"status": "healthy"}

    return {"status": "unhealthy"}  