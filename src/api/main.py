from fastapi import FastAPI, Depends, HTTPException
from app.services.chat_service import chat_pipeline
from schemas.chat import ChatRequest, ChatResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Personal chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "https://sumitlasiwa.com.np"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_chat_service():
    return chat_pipeline

    
@app.get("/")
def root():
    return {"message": "Personal chatbot"}

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "chatbot-api"
    }
        
@app.post("/chats", response_model=ChatResponse)
def chat(req: ChatRequest, pipeline = Depends(get_chat_service)):
    
    try:
        response = pipeline(req.user_id, req.query)
        
        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))