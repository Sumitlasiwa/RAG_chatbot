from langchain_community.document_loaders import PyPDFLoader, TextLoader 
import os
from langchain_core.documents import Document
from typing import List


def load_file(file_path: str) -> List[Document]:
    """
    load document content along with metadata

    Args:
        file_name (str): file path either .pdf or .txt

    Returns:
        list: parsed document content with metadata
    """
    # validate file exits
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # check file extension
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path=file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path=file_path)
    else:
        error_msg = f"Unsupported file type: {ext}. Only .pdf and .txt are supported."
        raise ValueError(error_msg)

    docs = list(loader.load()) # Load documents

    return docs
