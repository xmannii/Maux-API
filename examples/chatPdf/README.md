# Chat with PDF

🚀 This example demonstrates how to use the PDF extraction and embedding APIs to chat with a PDF file.

## Prerequisites

- Python 
- ChromaDB
- requests
- groq

## Installation

1. install requirements
```bash
pip install -r requirements.txt
```

2. run the self-hosted Maux-API server
```bash
uvicorn app.main:app --reload
```
3. add your groq api key to the env file
4. run the chat script
```bash
python chat.py
```

5. enter the path to your PDF file
6. enter your question
7. wait for the chat to end

