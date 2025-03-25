from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Header
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
    x_api_key: str = Header(..., alias="X-API-Key")
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        contents = await file.read()
        
        # Initialize RAG service with user's API key but your Supabase credentials
        rag_service = RAGService(
            google_api_key=x_api_key,  # Use the user's API key
            supabase_url=settings.supabase_url,  # Use your Supabase URL
            supabase_service_key=settings.supabase_service_key  # Use your Supabase key
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
async def chat(
    request: ChatRequest,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    try:
        # Get existing RAG service or create new one
        rag_service = app_state.get_rag_service()
        
        if not rag_service:
            # Create new RAG service with user's API key but your Supabase credentials
            rag_service = RAGService(
                google_api_key=x_api_key,  # Use the user's API key
                supabase_url=settings.supabase_url,  # Use your Supabase URL
                supabase_service_key=settings.supabase_service_key  # Use your Supabase key
            )
            app_state.set_rag_service(rag_service)
        else:
            # Update the existing RAG service with the new API key
            rag_service.google_api_key = x_api_key
        
        response = await rag_service.chat(request.question)
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