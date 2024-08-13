import asyncio
import chromadb
import requests
from typing import List

# FastAPI server URL
API_BASE_URL = "http://localhost:8000"  # Adjust if your FastAPI server is on a different address

async def extract_pdf_content(file_path: str) -> List[str]:
    """Extract content from a PDF file using the FastAPI endpoint."""
    with open(file_path, 'rb') as file:
        response = requests.post(f"{API_BASE_URL}/extract", files={"file": file})
    
    if response.status_code != 200:
        raise Exception(f"Failed to extract PDF content: {response.text}")
    
    # Extract the text from each page's content
    return [content['text'] for content in response.json()['content']]

async def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Get embeddings for a list of texts using the FastAPI endpoint."""
    embeddings = []
    for text in texts:
        response = requests.post(f"{API_BASE_URL}/embed", json={"text": text})
        if response.status_code != 200:
            raise Exception(f"Failed to get embedding: {response.text}")
        
        # Print the response for debugging
        print(response.json())
        
        # Access the embedding from the response
        embeddings.append(response.json()['data'][0]['embedding'])  # Adjusted to match the new response structure
    return embeddings

def setup_chroma():
    """Set up and return a Chroma client and collection."""
    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection(name="pdf_collection")
    return collection

async def process_pdf(file_path: str, collection):
    """Process a PDF file: extract content, generate embeddings, and store in Chroma."""
    print("Extracting PDF content...")
    pages = await extract_pdf_content(file_path)
    print(f"Extracted {len(pages)} pages.")
    print("Generating embeddings...")
    embeddings = await get_embeddings(pages)
    
    print("Storing in Chroma...")
    collection.add(
        embeddings=embeddings,
        documents=pages,
        ids=[f"page_{i + 1}" for i in range(len(pages))]  # Start IDs from 1 for better readability
    )
    print("PDF processed and stored in Chroma.")

async def chat_loop(collection):
    """Main chat loop for querying the stored PDF content."""
    while True:
        query = input("\nEnter your question (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        
        print("Generating query embedding...")
        query_embedding = await get_embeddings([query])
        
        print("Querying Chroma...")
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=2
        )
        
        print("\nMost relevant content:")
        for doc in results['documents'][0]:
            print(f"- {doc}\n")

async def main():
    collection = setup_chroma()
    
    file_path = input("Enter the path to your PDF file: ")
    await process_pdf(file_path, collection)
    
    print("\nPDF processed. Entering chat mode.")
    await chat_loop(collection)

if __name__ == "__main__":
    asyncio.run(main())