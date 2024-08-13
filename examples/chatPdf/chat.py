
import asyncio
from services.pdf_extractor import extract_pdf_content
from services.embedding_service import get_embeddings
from services.chroma_service import setup_chroma, store_in_chroma
from services.chat_service import chat_loop

async def process_pdf(file_path: str, collection):
    """Process a PDF file: extract content, generate embeddings, and store in Chroma."""
    print("Extracting PDF content...")
    pages = extract_pdf_content(file_path)
    print(f"Extracted {len(pages)} pages.")
    print("Generating embeddings...")
    embeddings = await get_embeddings(pages)
    
    print("Storing in Chroma...")
    store_in_chroma(collection, embeddings, pages)
    print("PDF processed and stored in Chroma.")

async def main():
    collection = setup_chroma()
    
    file_path = input("Enter the path to your PDF file: ")
    ## file_path = "example.pdf"
    await process_pdf(file_path, collection)
    
    print("\nPDF processed. Entering chat mode.")
    await chat_loop(collection)

if __name__ == "__main__":
    asyncio.run(main())
