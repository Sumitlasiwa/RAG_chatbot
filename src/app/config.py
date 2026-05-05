from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    mongodb_uri: str = Field(alias="MONGODB_URI")
    pinecone_token: str = Field(alias="PINECONE_TOKEN")
    redis_url: str = Field(alias="REDIS_URL")

    pinecone_index_name: str = "documentstore"
    embedding_model_name: str = "BAAI/bge-small-en-v1.5"
    embedding_dimension: int = 384
    llm_repo_id: str = "Qwen/Qwen2.5-7B-Instruct"
    huggingfacehub_api_token: str = Field(
        validation_alias=AliasChoices(
            "HUGGINGFACEHUB_API_TOKEN",
            "HUGGINGFACEHUB_ACCESS_TOKEN",
            "HF_TOKEN",
        )
    )

    chunk_size: int = 400
    chunk_overlap: int = 50
    batch_size: int = 50


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
