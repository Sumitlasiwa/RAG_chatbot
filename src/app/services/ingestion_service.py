import os
from langchain_community.embeddings import HuggingFaceEmbeddings


from dotenv import load_dotenv

load_dotenv()



from src.app.utils.file_loader import load_file
from src.app.utils.chunking import chunk_file

# load documnet
document = load_file(r"C:\Users\Lenovo\Desktop\Chatbot\notebooks\DM.pdf")

# Chunk document
chunks = chunk_file(document=document, chunker="RC", chunk_size=800, chunk_overlap=150)





embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"         # output_dimension = 384
)


from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
pc = Pinecone(api_key=os.environ["PINECONE_TOKEN"])


# create index (only once)
collection_name = "documentstore"
if collection_name not in pc.list_indexes().names():
    pc.create_index(
        collection_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
        )

# connect
index = pc.Index(collection_name)

vector_store = PineconeVectorStore(
    index=index,
    embedding=embedding_model,
    text_key="text"
)

from pymongo import MongoClient
uri = "mongodb+srv://lsumit008_db_user:gEiEiMhWtNFDZLti@cluster0.urpf1gy.mongodb.net/"
try:
    client = MongoClient(uri)

    # Test connection
    print("Successfully connected!")

except Exception as e:
    print("Connection failed:", e)
    
print(client.list_database_names())

db = client["doc_database"]
collection = db["metadata"]

from langchain_core.documents import Document
import uuid
import os



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

    # store everything in vector DB
    vector_store.add_documents([doc])   

    # store only document-level info in MongoDB
    collection.insert_one(cleaned_metadata)