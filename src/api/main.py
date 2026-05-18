from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.chat import router as chat_router
from api.routes.ingestion import router as ingestion_router
from api.routes.health import router as health_router

 
app = FastAPI(title="RAG chatbot APIs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", 
                   "https://sumitlasiwa.com.np", 
                   "http://localhost:5500", 
                   "https://www.sumitlasiwa.com.np"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"Detail" : "Chatbot api by Sumit"}

app.include_router(health_router)
app.include_router(chat_router)
app.include_router(ingestion_router)


    
    

        
