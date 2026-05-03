from pydantic import BaseModel
from pydantic import Field
from datetime import datetime

class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length = 1)
    content_type: str
    content: str   = Field(min_length = 1)
    word_count: int = Field(gt = 0)

class DocumentResponse(DocumentCreate):
    id: int
    deleted_at: datetime | None = None





