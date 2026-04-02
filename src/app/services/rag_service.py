

from src.app.services.ingestion_service import vector_store

retriever = vector_store.as_retriever(search="similarity", search_kwargs={"k":4})

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
)
llm = ChatHuggingFace(llm=llm)


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# chat template
chat_template = ChatPromptTemplate([
    ('system', "You are a helpful assistant. Answer ONLY from the conversation history and provided context. If insufficient info, say you don't know."),
    MessagesPlaceholder(variable_name='chat_history'),
    ('system', "context: {context}"),
    ('human', '{query}')
])

def format_docs(retrieved_docs):
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
    return context_text

from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from operator import itemgetter

# RunnableParallel gives same input to all keys so we used itemgetter to get only required inputs
context_question_chain = RunnableParallel({
    "context": itemgetter("query") | retriever | RunnableLambda(format_docs),
    "query": itemgetter("query"),
    "chat_history": itemgetter("chat_history")
})

from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

chain = context_question_chain | chat_template | llm | parser 