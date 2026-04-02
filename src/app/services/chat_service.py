import redis

from src.app.services.rag_service import chain

r = redis.Redis("localhost", port=6379, db=0)

import json
from langchain.messages import HumanMessage, AIMessage
def save_message(user_id, query, response):
    key = f"chat:{user_id}"
    r.rpush(key, json.dumps({"role": "human", "content": query}))
    r.rpush(key, json.dumps({"role": "ai", "content": response}))
    
    r.ltrim(key, -10, -1)   # keep only last 10 messages
    r.expire(key, 3600)     # delete messages after 1hr
    
def llm_generate(query, chat_history):
    return chain.invoke({
    "query": query,
    "chat_history": chat_history
})
    
def get_history(user_id):
    key = f"chat:{user_id}"
    raw_messages =  r.lrange(key, 0, -1)
    
    chat_history = []
    for msg in raw_messages:
        msg = json.loads(msg)
        
        if msg["role"] == "human":
            chat_history.append(HumanMessage(content=msg["content"]))
        if msg["role"] == "ai":
            chat_history.append(AIMessage(content=msg["content"]))
        
    return chat_history


def chat_pipeline(user_id, query):
    chat_history = get_history(user_id)
    response = llm_generate(query, chat_history)
    save_message(user_id, query, response)
   
    print(response)
    
chat_pipeline(123, "What is my name and age ?")