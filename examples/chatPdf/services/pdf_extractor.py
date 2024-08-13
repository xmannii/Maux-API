

import requests
from typing import List

API_BASE_URL = "http://localhost:8000"  # your maux api url here

def extract_pdf_content(file_path: str) -> List[str]:
    """Extract content from a PDF file using the FastAPI endpoint."""
    with open(file_path, 'rb') as file:
        response = requests.post(f"{API_BASE_URL}/extract", files={"file": file})
    
    if response.status_code != 200:
        raise Exception(f"Failed to extract PDF content: {response.text}")
    
    # Extract the text from each page's content
    return [content['text'] for content in response.json()['content']]
