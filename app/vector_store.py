from functools import lru_cache
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from app.config import get_settings


@lru_cache
def get_vector_store() -> Chroma :
    """The Chroma collection on disk, opened once and shared by ingestion and search."""
    settings = get_settings()
    embeddings = OpenAIEmbeddings(
        api_key=settings.hcr_openai_api_key.get_secret_value(),
        model=settings.embedding_model,
        check_embedding_ctx_length=False,  # skips tiktoken and its first-time download
        timeout=30,
        base_url=settings.openai_base_url
    )
    return Chroma(
        collection_name=settings.collection_name,
        embedding_function=embeddings,
        persist_directory=settings.chroma_dir,       # e.g. "data/chroma"
        collection_metadata={"hnsw:space": "cosine"} # cosine instead of default L2
    )
