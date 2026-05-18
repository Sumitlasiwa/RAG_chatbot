from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List


def chunk_file(document, chunker: str = "RecursiveCharacterTextSplitter", chunk_size=250, chunk_overlap=40) -> List[Document]:
    """chunks single document file into multiple small chunks

    Args:
        document (_type_): loaded document file to chunk
        chunker (str, optional): Chunker type select (RecursiveCharacterTextSplitter or CharacterTextSplitter). Defaults to "RecursiveCharacterTextSplitter".
        chunk_size (int): size of each chunk
        chunk_overlap (int): overlap tokens between each chunk sequences

    Returns:
        List[Document]: list of chunks of document
    """
    
    if chunker == "RecursiveCharacterTextSplitter":
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap,
        separators=["---", "#", "\n\n"])
    elif chunker == "CharacterTextSplitter":
        splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separator='')
        
    else:
        error_msg = f"Unsupported chunker: {chunker}. Select RecursiveCharacterTextSplitter or CharacterTextSplitter"
        raise ValueError(error_msg)
        

    chunks = splitter.split_documents(document)
    
    return chunks

# print(len(chunks))
# print(chunks[0].page_content)
# print(chunks[0].metadata)