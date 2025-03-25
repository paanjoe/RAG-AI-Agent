from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.services.rag_service import RAGService
from app.services.state import AppState
from app.config import settings
from typing import Dict, Any, Optional

router = APIRouter()
app_state = AppState.get_instance()

# Add this class for request validation
class ChatRequest(BaseModel):
    question: str

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),  # Use File(...) to properly handle multipart/form-data
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        contents = await file.read()
        
        # Initialize RAG service
        rag_service = RAGService(
            google_api_key=settings.google_api_key,
            supabase_url=settings.supabase_url,
            supabase_service_key=settings.supabase_service_key
        )
        
        # Process the PDF
        result = await rag_service.process_pdf(contents)
        
        # Store the RAG service in the app state
        app_state.set_rag_service(rag_service)
        
        return result
    except Exception as e:
        print(f"Error processing upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await file.close()

@router.post("/chat")
async def chat(request: ChatRequest):  # Change parameter type
    rag_service = app_state.get_rag_service()
    if rag_service is None:
        raise HTTPException(
            status_code=400, 
            detail="No PDF has been processed. Please upload a PDF first."
        )
    
    try:
        response = await rag_service.get_response(request.question)
        return {"response": response}
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_status():
    rag_service = app_state.get_rag_service()
    return {
        "has_rag_service": rag_service is not None,
        "has_chat_chain": rag_service and rag_service.chat_chain is not None if rag_service else False
    }