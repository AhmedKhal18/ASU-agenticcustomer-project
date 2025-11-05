"""Data ingestion pipeline for processing documents and creating vector embeddings."""
import os
import sys
from pathlib import Path
from typing import List, Dict
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings


def load_documents(data_dir: str) -> List[Document]:
    """Load documents from the data directory."""
    documents = []
    data_path = Path(data_dir)
    
    if not data_path.exists():
        print(f"Data directory {data_dir} does not exist. Creating it...")
        data_path.mkdir(parents=True, exist_ok=True)
        return documents
    
    # Supported file extensions
    supported_extensions = {'.txt', '.pdf', '.docx'}
    
    for file_path in data_path.rglob('*'):
        if file_path.suffix.lower() in supported_extensions:
            try:
                if file_path.suffix.lower() == '.txt':
                    loader = TextLoader(str(file_path), encoding='utf-8')
                elif file_path.suffix.lower() == '.pdf':
                    loader = PyPDFLoader(str(file_path))
                elif file_path.suffix.lower() == '.docx':
                    loader = Docx2txtLoader(str(file_path))
                else:
                    continue
                
                docs = loader.load()
                # Add metadata about source file
                for doc in docs:
                    doc.metadata['source'] = str(file_path)
                    doc.metadata['file_type'] = file_path.suffix.lower()[1:]
                
                documents.extend(docs)
                print(f"Loaded {len(docs)} documents from {file_path.name}")
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    
    return documents


def categorize_documents(documents: List[Document]) -> Dict[str, List[Document]]:
    """Categorize documents by type for different agents."""
    categorized = {
        'billing': [],
        'technical': [],
        'policy': []
    }
    
    for doc in documents:
        source_lower = doc.metadata.get('source', '').lower()
        content_lower = doc.page_content.lower()
        
        # Categorize based on file path or content
        if 'billing' in source_lower or 'invoice' in source_lower or 'pricing' in source_lower:
            doc.metadata['category'] = 'billing'
            categorized['billing'].append(doc)
        elif 'policy' in source_lower or 'terms' in source_lower or 'privacy' in source_lower or 'compliance' in source_lower:
            doc.metadata['category'] = 'policy'
            categorized['policy'].append(doc)
        elif 'technical' in source_lower or 'support' in source_lower or 'bug' in source_lower or 'forum' in source_lower:
            doc.metadata['category'] = 'technical'
            categorized['technical'].append(doc)
        else:
            # Default categorization based on content keywords
            if any(keyword in content_lower for keyword in ['billing', 'invoice', 'payment', 'subscription', 'price']):
                doc.metadata['category'] = 'billing'
                categorized['billing'].append(doc)
            elif any(keyword in content_lower for keyword in ['policy', 'terms', 'privacy', 'compliance', 'legal']):
                doc.metadata['category'] = 'policy'
                categorized['policy'].append(doc)
            else:
                doc.metadata['category'] = 'technical'
                categorized['technical'].append(doc)
    
    return categorized


def create_vector_store(documents: List[Document], collection_name: str, embeddings) -> Chroma:
    """Create or update a ChromaDB vector store."""
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    splits = text_splitter.split_documents(documents)
    print(f"Split documents into {len(splits)} chunks")
    
    # Create persistent ChromaDB
    chroma_db = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=settings.chroma_db_path,
        collection_name=collection_name,
    )
    
    return chroma_db


def main():
    """Main ingestion function."""
    print("Starting data ingestion pipeline...")
    
    # Check for OpenAI API key
    if not settings.openai_api_key:
        print("ERROR: OPENAI_API_KEY not set in environment variables")
        print("Please set it in your .env file or environment")
        sys.exit(1)
    
    # Initialize embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
    
    # Load documents
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    documents = load_documents(data_dir)
    
    if not documents:
        print("No documents found. Please add documents to the data/ directory")
        print("Supported formats: .txt, .pdf, .docx")
        return
    
    print(f"\nLoaded {len(documents)} total documents")
    
    # Categorize documents
    categorized = categorize_documents(documents)
    print(f"\nCategorized documents:")
    print(f"  - Billing: {len(categorized['billing'])}")
    print(f"  - Technical: {len(categorized['technical'])}")
    print(f"  - Policy: {len(categorized['policy'])}")
    
    # Create vector stores for each category
    for category, docs in categorized.items():
        if docs:
            print(f"\nCreating vector store for {category} documents...")
            collection_name = f"{settings.chroma_collection_name}_{category}"
            create_vector_store(docs, collection_name, embeddings)
            print(f"Vector store created for {category}")
    
    print("\nData ingestion complete!")


if __name__ == "__main__":
    main()

