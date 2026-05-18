from fastapi import APIRouter, Depends, HTTPException
from app.services.chat_service import chat_pipeline
from schemas.chat import ChatRequest, ChatResponse


router = APIRouter()

# Dependency
def get_chat_service():
    return chat_pipeline


@router.post("/chats", response_model=ChatResponse)
def chat(req: ChatRequest, pipeline = Depends(get_chat_service)):
    
    try:
        response = pipeline(req.user_id, req.query)
        
        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))