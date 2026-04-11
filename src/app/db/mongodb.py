from functools import lru_cache
from src.app.config import MONGODB_URI as uri
from pymongo import MongoClient


@lru_cache(maxsize=1)
def get_mongodb_collection():
    
    if not uri:
        raise ValueError("MongoDB_URI is not configured")
    
    try:
        client = MongoClient(uri)
        db = client["doc_database"]
        return db["metadata"]


    except Exception as e:
        raise ConnectionError(f"Failed to connect to MongoDB: {e}") 
            
