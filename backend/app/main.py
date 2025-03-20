from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import document

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "RAG AI API is running"}