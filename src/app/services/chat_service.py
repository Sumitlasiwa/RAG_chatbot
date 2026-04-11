from src.app.services.rag_service import rag_chain
from src.app.db.redis_client import get_history, save_message
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

def chat_pipeline(user_id, query):
    chat_history = get_history(user_id)
    response = llm_generate(query, chat_history)
    save_message(user_id, query, response)
    
    return response
       
# chat_pipeline(123, "What is my name and age ?")