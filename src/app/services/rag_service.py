from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from operator import itemgetter
from src.app.services.ingestion_service import vector_store
from src.app.db.vector_db import retriever
from src.app.utils.prompt_builder import chat_template

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
)
llm = ChatHuggingFace(llm=llm)

def format_docs(retrieved_docs):
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
    return context_text

# RunnableParallel gives same input to all keys so we used itemgetter to get only required inputs
context_question_chain = RunnableParallel({
    "context": itemgetter("query") | retriever | RunnableLambda(format_docs),
    "query": itemgetter("query"),
    "chat_history": itemgetter("chat_history")
})

from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

chain = context_question_chain | chat_template | llm | parser 