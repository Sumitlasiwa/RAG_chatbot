from functools import lru_cache
from pinecone import ServerlessSpec, Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.app.config import EMBEDDING_MODEL_NAME, PINECONE_INDEX_NAME, PINECONE_TOKEN


@lru_cache(maxsize=1)
def get_vectorstore():
    
    embedding_model = HuggingFaceEmbeddings(
model_name=EMBEDDING_MODEL_NAME)
    pc = Pinecone(api_key=PINECONE_TOKEN)
    
    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            PINECONE_INDEX_NAME,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
            )

    # connect
    index = pc.Index(PINECONE_INDEX_NAME)

    
    
    vector_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        text_key="text"
    )

    return vector_store

def get_retriever():
    retriever = get_vectorstore().as_retriever(search="similarity", search_kwargs={"k":4})
    
    return retriever
    
