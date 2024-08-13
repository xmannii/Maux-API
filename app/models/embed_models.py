from pydantic import BaseModel
from typing import List

class EmbedRequest(BaseModel):
    text: str

class EmbeddingData(BaseModel):
    object: str = "embedding"
    index: int
    embedding: List[float]

class EmbeddingResponse(BaseModel):
    object: str = "list"
    data: List[EmbeddingData]
    model: str