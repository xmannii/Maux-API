
import os
from groq import Groq
from services.embedding_service import get_embeddings
from services.chroma_service import query_chroma

# Initialize the Groq client with the API key 
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

async def chat_loop(collection):
    """Main chat loop for querying the stored PDF content and interacting with Groq API."""
    messages = [{"role": "system", "content": "You are a helpful assistant that answers questions based on the extracted content from a PDF file."}]
    
    while True:
        query = input("\nEnter your question (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        
        print("Generating query embedding...")
        query_embedding = await get_embeddings([query])
        
        print("Querying Chroma...")
        results = query_chroma(collection, query_embedding)
        print(results)
        if not results['documents']:
            print("No relevant content found in the PDF.")
            continue
       
        # Prepare the prompt template
        top_documents = results['documents'][0][:2]  # Get top 2 results
        prompt = "The following are the most relevant contents extracted from the PDF:\n"
        for i, doc in enumerate(top_documents, 1):
            prompt += f"{i}. {doc}\n"
        prompt += f"\nUser Question: {query}\n\nPlease provide a response based on the extracted content."
        print(prompt)
        # Add the user message to the messages list
        messages.append({"role": "user", "content": prompt})
        
        # Generate a response from Groq API
        print("Generating response from Groq API...")
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.1-70b-versatile",
        )
        
        response_content = chat_completion.choices[0].message.content
        print(f"\nAI Response:\n{response_content}")
        
        # Add the AI's response to the messages list
        messages.append({"role": "assistant", "content": response_content})

