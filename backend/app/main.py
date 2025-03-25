from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import document

app = FastAPI()

# More permissive CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=False,  # Must be False if allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document.router, prefix="/api")

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