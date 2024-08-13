# services/embedding_service.py

import requests
from typing import List

API_BASE_URL = "http://localhost:8000"  # your maux api url here
async def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Get embeddings for a list of texts using the FastAPI endpoint."""
    embeddings = []
    for text in texts:
        response = requests.post(f"{API_BASE_URL}/embed", json={"text": text})
        if response.status_code != 200:
            raise Exception(f"Failed to get embedding: {response.text}")
        
        # Access the embedding from the response
        embeddings.append(response.json()['data'][0]['embedding'])  
    return embeddings
