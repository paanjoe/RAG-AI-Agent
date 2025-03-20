from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import document

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://rag-ai-agent-nyxuzdk4o-farhan-fazlis-projects.vercel.app/"  # Add your deployed frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document.router)

@app.get("/")
async def root():
    return {"message": "RAG AI API is running"}

@app.get("/api/routes")
async def list_routes():
    routes = []
    for route in app.routes:
        routes.append({
            "path": route.path,
            "methods": route.methods
        })
    return {"routes": routes}