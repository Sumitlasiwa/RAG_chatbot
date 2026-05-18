from functools import lru_cache
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_core.embeddings import Embeddings
from app.config import get_settings

settings = get_settings()


class PineconeHostedEmbeddings(Embeddings):
    def __init__(self, client: Pinecone, model_name: str, dimension: int):
        self.client = client
        self.model_name = model_name
        self.dimension = dimension

    @staticmethod
    def _values_from_embedding(item):
        if hasattr(item, "values"):
            return list(item.values)
        return list(item["values"])

    def _embed(self, inputs: list[str], input_type: str) -> list[list[float]]:
        if not inputs:
            return []

        embeddings = self.client.inference.embed(
            model=self.model_name,
            inputs=inputs,
            parameters={
                "input_type": input_type,
                "truncate": "END",
                "dimension": self.dimension,
            },
        )
        return [self._values_from_embedding(item) for item in embeddings.data]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embed(texts, input_type="passage")

    def embed_query(self, text: str) -> list[float]:
        return self._embed([text], input_type="query")[0]


@lru_cache(maxsize=1)
def get_pinecone_client():
    return Pinecone(api_key=settings.pinecone_token)


@lru_cache(maxsize=1)
def get_embedding_model():
    return PineconeHostedEmbeddings(
        client=get_pinecone_client(),
        model_name=settings.embedding_model_name,
        dimension=settings.embedding_dimension,
    )


def _validate_index_dimension(pc: Pinecone) -> None:
    if not pc.has_index(settings.pinecone_index_name):
        raise ValueError(
            f"Pinecone index '{settings.pinecone_index_name}' does not exist. "
            "Create it before starting the API or run the ingestion CLI to "
            "create it automatically."
        )

    index_description = pc.describe_index(settings.pinecone_index_name)
    if index_description.dimension != settings.embedding_dimension:
        raise ValueError(
            f"Pinecone index '{settings.pinecone_index_name}' has dimension "
            f"{index_description.dimension}, but EMBEDDING_DIMENSION is "
            f"{settings.embedding_dimension}."
        )


def ensure_pinecone_index(create_if_missing: bool = False) -> None:
    pc = get_pinecone_client()

    if not pc.has_index(settings.pinecone_index_name):
        if not create_if_missing:
            raise ValueError(
                f"Pinecone index '{settings.pinecone_index_name}' does not exist. "
                "Create it before starting the API or run the ingestion CLI to "
                "create it automatically."
            )

        pc.create_index(
            name=settings.pinecone_index_name,
            dimension=settings.embedding_dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=settings.pinecone_cloud,
                region=settings.pinecone_region,
            ),
            timeout=300,
        )

    _validate_index_dimension(pc)


@lru_cache(maxsize=1)
def get_vectorstore():
    pc = get_pinecone_client()
    _validate_index_dimension(pc)

    vector_store = PineconeVectorStore(
        index=pc.Index(settings.pinecone_index_name),
        embedding=get_embedding_model(),
        text_key="text",
    )

    return vector_store


def get_retriever():
    retriever = get_vectorstore().as_retriever(
        search="similarity",
        search_kwargs={"k": 4},
    )
    return retriever
