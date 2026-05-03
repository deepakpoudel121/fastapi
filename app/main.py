from app.routes import documents_router
from fastapi import FastAPI
from fastapi import Depends
from app.db.connection import get_db_connection 
from models import DocumentRequest
from app.core import logger
import time

app = FastAPI()

app.include_router(documents_router)

@app.middleware('http')
def log_requests(request: DocumentRequest, call_next):
    start_time = time.time()
    response = call_next(request)
    latency_ms = round((time.time() - start_time) * 1000, 2)
    logger.info(
        'request',
         extra={
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "latency_ms": latency_ms,
        }

    )
    return response

@app.get("/")
async def root():   
    try: 
        return {"message": "Welcome to the Document Retrieval API"}
    except Exception as e:
        return {"message": "An error occurred", "error": str(e)}

@app.get("/health")
async def health_check(db = Depends(get_db_connection)):
    try: 
        with db.cursor() as cur:
            cur.execute("SELECT 1")
            result = cur.fetchone()
            if result and result[0] == 1:    
                return {"status": "healthy"}

        return {"status": "unhealthy"}  
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}