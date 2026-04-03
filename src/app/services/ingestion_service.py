import os
from langchain_core.documents import Document
import uuid
from dotenv import load_dotenv

load_dotenv()

from src.app.utils.file_loader import load_file
from src.app.utils.chunking import chunk_file
from src.app.db.vector_db import vector_store
from src.app.db.mongodb import collection
from src.app.db.mongodb import save_metadata
from src.app.db.vector_db import add_documents

# load documnet
document = load_file(r"C:\Users\Lenovo\Desktop\Chatbot\notebooks\DM.pdf")

# Chunk document
chunks = chunk_file(document=document, chunker="RC", chunk_size=800, chunk_overlap=150)

# save vector to vectordb and metadata to NoSQL db for each chunk
for i, chunk in enumerate(chunks):
    doc_id = str(uuid.uuid4())
    file_name = os.path.basename(chunk.metadata.get("source", ""))
    
    cleaned_metadata = {
        "doc_id":doc_id,
        "file_name": file_name,
        "page": chunk.metadata.get("page"),
        "total_pages": chunk.metadata.get("total_pages"),
        "chunk_index": i
    }
    doc = Document(
        page_content=chunk.page_content,
        metadata=chunk.metadata
    )
    
    add_documents(doc)   # store everything in vector DB
    
    save_metadata(cleaned_metadata)     # store only document-level info in MongoDB

    