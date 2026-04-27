import json
from langchain.messages import HumanMessage, AIMessage
import redis
from app.config import get_settings
from functools import lru_cache
settings = get_settings()
@lru_cache(maxsize=1)
def get_redis_client():
    return redis.Redis(host=settings.redis_host,
                       port=settings.redis_port,
                       db=settings.redis_db)

def save_message(user_id, query, response):
    r = get_redis_client()
    key = f"chat:{user_id}"
    messages = [
        json.dumps({"role": "human", "content": query}),
        json.dumps({"role": "ai", "content": response})
    ]
    r.rpush(key, *messages)
    r.ltrim(key, -20, -1)   # keep only last 10 conversation pairs
    r.expire(key, 3600)     # delete messages after 1hr
    
def get_history(user_id):
    r = get_redis_client()
    key = f"chat:{user_id}"
    raw_messages =  r.lrange(key, 0, -1)
    
    chat_history = []
    for msg in raw_messages:
        if isinstance(msg, bytes):
            msg = msg.decode("utf-8")
            
        msg = json.loads(msg)
        
        if msg["role"] == "human":
            chat_history.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "ai":
            chat_history.append(AIMessage(content=msg["content"]))
        
    return chat_history