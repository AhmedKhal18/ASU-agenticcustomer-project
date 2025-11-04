"""Vector store utilities for ChromaDB."""
import os
from typing import List, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from config import settings


def get_vector_store(collection_name: str) -> Optional[Chroma]:
    """Get a ChromaDB vector store instance."""
    if not os.path.exists(settings.chroma_db_path):
        return None
    
    embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
    
    try:
        vector_store = Chroma(
            persist_directory=settings.chroma_db_path,
            embedding_function=embeddings,
            collection_name=collection_name,
        )
        return vector_store
    except Exception as e:
        print(f"Error loading vector store: {e}")
        return None


def get_retriever(collection_name: str, k: int = 5) -> Optional[object]:
    """Get a retriever for a specific collection."""
    vector_store = get_vector_store(collection_name)
    if vector_store:
        return vector_store.as_retriever(search_kwargs={"k": k})
    return None


def search_documents(query: str, collection_name: str, k: int = 5) -> List[Document]:
    """Search for documents in a collection."""
    vector_store = get_vector_store(collection_name)
    if not vector_store:
        return []
    
    try:
        results = vector_store.similarity_search(query, k=k)
        return results
    except Exception as e:
        print(f"Error searching documents: {e}")
        return []

