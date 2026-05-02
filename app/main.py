from app.routes import documents_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(documents_router)

@app.get("/")
async def root():    return {"message": "Welcome to the Document Retrieval API"}

@app.get("/health")
async def health_check():    return {"status": "healthy"}

