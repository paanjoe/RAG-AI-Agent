from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.services.rag_service import RAGService
from app.config import settings
from typing import Dict, Any, Optional

router = APIRouter()
rag_service = None

# Add this class for request validation
class ChatRequest(BaseModel):
    question: str

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),  # Use File(...) to properly handle multipart/form-data
):
    global rag_service
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        contents = await file.read()
        
        # Initialize RAG service if not already initialized
        if rag_service is None:
            rag_service = RAGService(
                google_api_key=settings.google_api_key,
                supabase_url=settings.supabase_url,
                supabase_service_key=settings.supabase_service_key
            )
        
        result = await rag_service.process_pdf(contents)
        return JSONResponse(content=result)
        
    except Exception as e:
        print(f"Error processing upload: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await file.close()

@router.post("/chat")
async def chat(request: ChatRequest):  # Change parameter type
    global rag_service
    if rag_service is None:
        raise HTTPException(status_code=400, detail="Please upload a PDF first")
    
    try:
        response = await rag_service.get_response(request.question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))