from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env")
    hcr_openai_api_key: SecretStr
    temperature: float
    llm_model: str
    embedding_model: str

    chunk_size: int = Field(default=800, gt=0)
    chunk_overlap: int = Field(default=100, ge=0)
    top_k: int = Field(default=4, gt=0)
    score_threshold: float = Field(default=0.3, ge=0, le=1)  # below this, results are ignored

    raw_docs_dir: str = "data/raw"
    chroma_dir: str = "data/chroma"
    collection_name: str = "help_center"
    anonymized_telemetry: bool = False
    openai_base_url: str = "https://api.openai.com/v1"


@lru_cache
def get_settings() -> Settings:
    return Settings()