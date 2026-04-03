from src.app.services.rag_service import chain
from src.app.db.redis_client import get_history, save_message

    
def llm_generate(query, chat_history):
    return chain.invoke({
    "query": query,
    "chat_history": chat_history
})

def chat_pipeline(user_id, query):
    chat_history = get_history(user_id)
    response = llm_generate(query, chat_history)
    save_message(user_id, query, response)
   
    print(response)
    
chat_pipeline(123, "What is my name and age ?")