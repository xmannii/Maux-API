from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.services.token_counter import count_tokens, SUPPORTED_MODELS

router = APIRouter()

class TokenCountRequest(BaseModel):
    content: str
    model: str = "gpt-3.5-turbo"
    token_limit: int = None

@router.post("/count")
async def count_tokens_route(request: TokenCountRequest):
    if request.model not in SUPPORTED_MODELS:
        raise HTTPException(status_code=400, detail=f"Unsupported model: {request.model}")

    try:
        num_tokens = count_tokens(request.content, request.model)
        response = {
            "model": request.model,
            "num_tokens": num_tokens
        }

        if request.token_limit is not None:
            within_limit = num_tokens <= request.token_limit
            response["token_limit"] = request.token_limit
            response["within_limit"] = within_limit

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting tokens: {str(e)}")