from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# chat template


chat_template = ChatPromptTemplate([
    ('system', "You are a helpful assistant. Answer ONLY from the conversation history and provided context. If insufficient info, say you don't know."),
    MessagesPlaceholder(variable_name='chat_history'),
    ('system', "context: {context}"),
    ('human', '{query}')
])
    
