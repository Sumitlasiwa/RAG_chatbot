import os
from langchain_core.documents import Document
import uuid
from tqdm import tqdm
from app.utils.file_loader import load_file
from app.utils.chunking import chunk_file
from app.db.mongodb import get_mongodb_collection
from app.db.vector_db import get_vectorstore
from app.config import get_settings
from pymongo import ReplaceOne

settings = get_settings()
def ingest_document(file_path: str, chunk_size = settings.chunk_size, chunk_overlap = settings.chunk_overlap, batch_size = settings.batch_size) -> dict: 
    """takes text or pdf file then does loading, chunking and saving  in batches chunks in vector db and nosql db

    Args:
        file_path (str): path of the input file
        chunk_size (int): size of each chunk
        chunk_overlap (int): overlap between sequence of chunks
        batch_size (int): batch size of each chunk for processing
        
    """
    file_name = os.path.basename(file_path)

    document_id = str(uuid.uuid4())
    # load documnet
    document = load_file(file_path)
    if not document:
        raise ValueError(f"No content loaded from file: {file_path}")
    
    # Chunk document
    chunks = chunk_file(document=document, chunker="RC", chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    if not chunks:
        raise ValueError(f"No chunks generated from file: {file_name}")
    
    
    # save vector to vectordb and metadata to NoSQL db for each batch of chunks
    
    vector_store = get_vectorstore()            # vector db connect
    collection = get_mongodb_collection()       # connect to mongodb and get collection
    
    collection.update_one(
        {"document_id": document_id},
        {"$set": {
            "document_id": document_id,
            "file_name": file_name,
            "status": "processing",
            "chunk_count": len(chunks),
        }},
        upsert=True,
    )

    try:
        for i in tqdm(range(0, len(chunks), batch_size), desc=f"Ingesting {file_name}"):
            
            batch = chunks[i:i+batch_size]
            
            docs_to_insert, metadata_to_insert = [], []
            
            for j, chunk in enumerate(batch):
                chunk_index = i + j
                chunk_id = f"{document_id}:{chunk_index}"
                
                chunk_metadata = {
                    **chunk.metadata,
                    "chunk_id": chunk_id,
                    "document_id": document_id,
                    "file_name": file_name,
                    # "page": chunk.metadata.get("page"),
                    # "total_pages": chunk.metadata.get("total_pages"),
                    "chunk_index": chunk_index,
                }

                docs_to_insert.append(Document(
                    page_content=chunk.page_content,
                    metadata=chunk_metadata,
                ))
                metadata_to_insert.append(
                    ReplaceOne(
                        {"chunk_id": chunk_id},
                        chunk_metadata,
                        upsert=True,
                    )
                )
            
            vector_store.add_documents(
                docs_to_insert,
                ids=[doc.metadata["chunk_id"] for doc in docs_to_insert],
            )
            collection.bulk_write(metadata_to_insert)    
                        
            collection.update_one(
            {"document_id": document_id},
            {"$set": {"status": "completed"}}
        )
            
        summary = {
            "chunks_inserted" : len(chunks),
            "file_name" : file_name
        }
        
        return summary
    
    except Exception as exc:
        collection.update_one(
            {"document_id": document_id},
            {"$set": {"status": "failed", "error": str(exc)}}
        )
        raise
        
if __name__ == "__main__":
    file_path = r"C:\Users\Lenovo\Desktop\Chatbot\books\DM.pdf"
    # ingest_document(file_path, CHUNK_SIZE, CHUNK_OVERLAP)

    