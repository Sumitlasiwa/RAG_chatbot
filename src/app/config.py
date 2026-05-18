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

    pinecone_index_name: str = Field(
        default="documentstore",
        alias="PINECONE_INDEX_NAME",
    )
    pinecone_cloud: str = Field(default="aws", alias="PINECONE_CLOUD")
    pinecone_region: str = Field(default="us-east-1", alias="PINECONE_REGION")
    embedding_model_name: str = Field(
        default="llama-text-embed-v2",
        alias="EMBEDDING_MODEL_NAME",
    )
    embedding_dimension: int = Field(default=384, alias="EMBEDDING_DIMENSION")
    llm_repo_id: str = Field(default="Qwen/Qwen2.5-7B-Instruct", alias="LLM_REPO_ID")
    huggingfacehub_api_token: str = Field(
        validation_alias=AliasChoices(
            "HUGGINGFACEHUB_API_TOKEN",
            "HUGGINGFACEHUB_ACCESS_TOKEN",
            "HF_TOKEN",
        )
    )

    chunk_size: int = Field(default=400, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=50, alias="CHUNK_OVERLAP")
    batch_size: int = Field(default=50, alias="BATCH_SIZE")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
