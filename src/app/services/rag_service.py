from langchain_core.runnables import RunnableParallel, RunnableLambda
from operator import itemgetter
from app.db.vector_db import get_retriever
from app.utils.prompt_builder import chat_template
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from app.config import get_settings
from langchain_core.output_parsers import StrOutputParser
from functools import lru_cache

settings = get_settings()
@lru_cache(maxsize=1)
def get_llm():
    chat_llm = HuggingFaceEndpoint(
    repo_id=settings.llm_repo_id,
    task="text-generation",
)
    return ChatHuggingFace(llm=chat_llm)

def rag_chain():
    llm = get_llm()
    retriever = get_retriever()
    def format_docs(retrieved_docs):
        context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
        return context_text

    # RunnableParallel gives same input to all keys so we used itemgetter to get only required inputs
    context_question_chain = RunnableParallel({
        "context": itemgetter("query") | retriever | RunnableLambda(format_docs),
        "query": itemgetter("query"),
        "chat_history": itemgetter("chat_history")
    })

    parser = StrOutputParser()

    chain = context_question_chain | chat_template | llm | parser 
    
    return chain