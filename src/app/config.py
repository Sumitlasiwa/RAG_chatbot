import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
PINECONE_TOKEN = os.getenv("PINECONE_TOKEN")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

PINECONE_INDEX_NAME = "documentstore"
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5" #output_dimension = 384
LLM_REPO_ID = "Qwen/Qwen2.5-7B-Instruct"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
BATCH_SIZE = 50
