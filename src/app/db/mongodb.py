from functools import lru_cache
from app.config import get_settings
from pymongo import MongoClient


settings = get_settings()
@lru_cache(maxsize=1)
def get_mongodb_collection():
    uri = settings.mongodb_uri
    if not uri:
        raise ValueError("MongoDB_URI is not configured")
    
    try:
        client = MongoClient(uri)
        db = client["doc_database"]
        return db["metadata"]


    except Exception as e:
        raise ConnectionError(f"Failed to connect to MongoDB: {e}") 
            
