from functools import lru_cache
from pinecone import ServerlessSpec, Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import get_settings

settings = get_settings()
@lru_cache(maxsize=1)
def get_embedding_model():
    return HuggingFaceEmbeddings(
model_name=settings.embedding_model_name)
    
@lru_cache(maxsize=1)
def get_vectorstore():
    pc = Pinecone(api_key=settings.pinecone_token)
    
    if settings.pinecone_index_name not in pc.list_indexes().names():
        pc.create_index(
            settings.pinecone_index_name,
            dimension=settings.embedding_dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
            )

    # connect
    index = pc.Index(settings.pinecone_index_name)

    
    
    vector_store = PineconeVectorStore(
        index=index,
        embedding=get_embedding_model(),
        text_key="text"
    )

    return vector_store

def get_retriever():
    retriever = get_vectorstore().as_retriever(search="similarity", search_kwargs={"k":4})
    
    return retriever
    
