from pydantic import BaseModel

class Document(BaseModel):
    id: int
    title: str
    content: str
    author: str
    content_type: str
    word_count: int



