from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import file_processing 
from app.routers import token_counter
from app.routers import embed_router
app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",  # Local development
    # add your origins here 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(file_processing.router)
app.include_router(token_counter.router)
## ommit this if you don't want to use the embedding API and download the model
app.include_router(embed_router.router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)