import json
from langchain.messages import HumanMessage, AIMessage
import redis
from src.app.config import REDIS_HOST, REDIS_PORT, REDIS_DB

def get_redis_client():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def save_message(user_id, query, response):
    r = get_redis_client()
    key = f"chat:{user_id}"
    r.rpush(key, json.dumps({"role": "human", "content": query}))
    r.rpush(key, json.dumps({"role": "ai", "content": response}))
    
    r.ltrim(key, -20, -1)   # keep only last 10 conversation pairs
    r.expire(key, 3600)     # delete messages after 1hr
    
def get_history(user_id):
    r = get_redis_client()
    key = f"chat:{user_id}"
    raw_messages =  r.lrange(key, 0, -1)
    
    chat_history = []
    for msg in raw_messages:
        msg = json.loads(msg)
        
        if msg["role"] == "human":
            chat_history.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "ai":
            chat_history.append(AIMessage(content=msg["content"]))
        
    return chat_history