from app.services.rag_service import rag_chain, get_llm
from app.db.redis_client import get_history, save_message
from app.db.vector_db import get_retriever
from functools import lru_cache


# creates the chain only the first time it's needed, then reuses it
@lru_cache(maxsize=1)
def get_chain():
    return rag_chain()

def llm_generate(query, chat_history):
    
    return get_chain().invoke({
    "query": query,
    "chat_history": chat_history
})

from typing import TypedDict, Annotated

class IsChitchat(TypedDict):
        
        chat_type : Annotated[bool, "Return exactly one of: \
            'True' for greetings or casual conversation/greetings/small talk, \
            'False' for everything else"]
        
@lru_cache(maxsize=1)
def get_chitchat_classifier():
    return get_llm().with_structured_output(IsChitchat)

def is_chitchat(query):
    return get_chitchat_classifier().invoke(query)["chat_type"]

def is_similar(query):
    retriever = get_retriever()
    docs = retriever.invoke(query)
    return bool(docs)
    

def chat_pipeline(user_id, query):
    chat_history = get_history(user_id)
    
    if is_chitchat(query) or is_similar(query):
        response = llm_generate(query, chat_history)
    else:
        response = "Question is out of my knowledge base. Let's talk about Sumit's portfolio"
        
    save_message(user_id, query, response)
    return response
    
       
