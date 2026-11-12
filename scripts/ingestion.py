from pathlib import Path

from hashlib import md5
from app.vector_store import get_vector_store
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader
from app.config import get_settings

chroma_db = get_vector_store()
settings = get_settings()

doc = PyPDFDirectoryLoader(settings.raw_docs_dir).load() # loads every PDF in the folder

splitter = RecursiveCharacterTextSplitter(
    chunk_size = settings.chunk_size,
    chunk_overlap = settings.chunk_overlap,

)

chunks = splitter.split_documents(doc)

# print(len(chunks))
# print(chunks[0].page_content)
# print(chunks[0].metadata)
# print("path ",chunks[0].metadata["source"])
# print("name ",Path(chunks[0].metadata["source"]).name)


# metadata:
for chunk in chunks:
    chunk.metadata["source"] = Path(chunk.metadata["source"]).name

# ids:
ids = [md5(f"{c.metadata['source']}:{c.page_content}".encode()).hexdigest() for c in chunks]

# chroma savings
chroma_db.add_documents(
    documents=chunks,
    ids=ids
)

print(f"Indexed {len(chunks)} chunks")