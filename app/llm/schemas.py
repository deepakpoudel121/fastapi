from pydantic import BaseModel
from typing import Literal


class StructuredOutput(BaseModel):
    summary: str
    key_topics: list[str]
    sentiment: Literal['positive', 'neutral', 'negative']
    suggested_tags: list[str]


class LLMResponse(BaseModel):
    document_id: int
    summary: str
    key_topics: list[str]
    sentiment: str
    suggested_tags: list[str]
    model_used: str
    latency_ms: int
    cost_usd: float = 0.0
