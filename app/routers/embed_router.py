from fastapi import APIRouter, HTTPException
from app.services.embedding_service import EmbeddingService
from app.models.embed_models import EmbedRequest, EmbeddingResponse
import numpy as np

router = APIRouter()

MODEL_NAME = "Alibaba-NLP/gte-multilingual-base" # good persian supporting model
embedding_service = EmbeddingService(MODEL_NAME)

@router.post("/embed", response_model=EmbeddingResponse)
async def embed_text(request: EmbedRequest):
    try:
        embedding = embedding_service.get_embedding(request.text)
        embedding_list = np.where(np.isnan(embedding), None, embedding).tolist()

        response = EmbeddingResponse(
            data=[
                {
                    "object": "embedding",
                    "index": 0,
                    "embedding": embedding_list,
                }
            ],
            model=MODEL_NAME
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))