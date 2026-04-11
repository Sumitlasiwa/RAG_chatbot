import os
from langchain_core.documents import Document
import uuid
from tqdm import tqdm
from src.app.utils.file_loader import load_file
from src.app.utils.chunking import chunk_file
from src.app.db.mongodb import get_mongodb_collection
from src.app.db.vector_db import get_vectorstore
from src.app.config import CHUNK_SIZE, CHUNK_OVERLAP, BATCH_SIZE

def ingest_document(file_path: str, chunk_size = 800, chunk_overlap = 150, batch_size = 50) -> dict: 
    """takes text or pdf file then does loading, chunking and saving  in batches chunks in vector db and nosql db

    Args:
        file_path (str): path of the input file
        chunk_size (int): size of each chunk
        chunk_overlap (int): overlap between sequence of chunks
        batch_size (int): batch size of each chunk for processing
        
    """
    file_name = os.path.basename(file_path)

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

    for i in tqdm(range(0, len(chunks), batch_size), desc=f"Ingesting {file_name}"):
        
        batch = chunks[i:i+batch_size]
        
        docs_to_insert, metadata_to_insert = [], []
        for j, chunk in enumerate(batch):
            doc_id = str(uuid.uuid4())
            
            chunk_metadata = {
                **chunk.metadata,
                "doc_id": doc_id,
                "file_name": file_name,
                "page": chunk.metadata.get("page"),
                "total_pages": chunk.metadata.get("total_pages"),
                "chunk_index": i + j,
            }

            doc = Document(
                page_content=chunk.page_content,
                metadata=chunk_metadata
            )
            
            docs_to_insert.append(doc)
            metadata_to_insert.append(chunk_metadata)
           
        vector_store.add_documents(docs_to_insert)   # store everything in vector DB
        
        collection.insert_many(metadata_to_insert)    # store only document-level info in MongoDB
        
    summary = {
        "chunks_inserted" : len(chunks),
        "file_name" : file_name
    }
    
    return summary
        
if __name__ == "__main__":
    file_path = r"C:\Users\Lenovo\Desktop\Chatbot\books\DM.pdf"
    ingest_document(file_path, CHUNK_SIZE, CHUNK_OVERLAP)

    