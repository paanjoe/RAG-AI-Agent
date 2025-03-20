from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from ..services.rag_service import RAGService
from ..config import settings
import io

router = APIRouter()
rag_service = RAGService(
    settings.google_api_key,
    settings.supabase_url,
    settings.supabase_service_key
)

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    contents = await file.read()
    result = await rag_service.process_pdf(contents)
    return JSONResponse(content=result)

@router.post("/chat")
async def chat(question: str):
    try:
        response = await rag_service.get_response(question)
        return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))