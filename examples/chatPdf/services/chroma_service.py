# services/chroma_service.py

import chromadb

def setup_chroma():
    """Set up and return a Chroma client and collection."""
    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection(name="pdf_collection")
    return collection

def store_in_chroma(collection, embeddings, documents):
    """Store embeddings and documents in Chroma."""
    collection.add(
        embeddings=embeddings,
        documents=documents,
        ids=[f"page_{i + 1}" for i in range(len(documents))]  # Start IDs from 1 for better readability
    )

def query_chroma(collection, query_embedding):
    """Query the Chroma collection."""
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=2
    )
    return results
