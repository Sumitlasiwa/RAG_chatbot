from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore


embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"         # output_dimension = 384
)

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

def add_documents(document):
    vector_store.add_documents([document])   # store everything in vector DB
    
retriever = vector_store.as_retriever(search="similarity", search_kwargs={"k":4})
    
