from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=r"C:\Users\Lenovo\Desktop\Chatbot\.env", env_file_encoding="utf-8")

    mongodb_uri: str
    pinecone_token: str
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    pinecone_index_name: str = "documentstore"
    embedding_model_name: str = "BAAI/bge-small-en-v1.5"
    embedding_dimension: int = 384
    llm_repo_id: str = "Qwen/Qwen2.5-7B-Instruct"
    huggingfacehub_access_token: str | None = None

    chunk_size: int = 800
    chunk_overlap: int = 150
    batch_size: int = 50


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
