"""Technical Support Agent - Pure RAG (Retrieval Augmented Generation)."""
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from llm_providers import get_generator_llm
from vector_store import search_documents


class TechnicalAgent:
    """Agent for handling technical support questions using Pure RAG."""
    
    def __init__(self):
        self.llm = get_generator_llm()
        self.collection_name = f"{self._get_collection_name()}_technical"
    
    def _get_collection_name(self) -> str:
        """Get the base collection name from settings."""
        from config import settings
        return settings.chroma_collection_name
    
    def _retrieve_context(self, question: str, k: int = 5) -> str:
        """Retrieve relevant context from vector store."""
        docs = search_documents(question, self.collection_name, k=k)
        
        if not docs:
            return "No relevant technical documentation found."
        
        context = "\n\n".join([
            f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}" 
            for doc in docs
        ])
        
        return context
    
    def _create_prompt(self) -> ChatPromptTemplate:
        """Create the prompt template for technical agent."""
        return ChatPromptTemplate.from_messages([
            ("system", """You are a Technical Support specialist for a customer service system.
Your role is to help customers with technical issues, bugs, and product-related questions.

Use the retrieved technical documentation to provide accurate solutions. If the documentation 
doesn't contain the answer, suggest troubleshooting steps or escalate to human support.

Be helpful, clear, and provide step-by-step instructions when possible."""),
            ("human", """Context from knowledge base:
{context}

User Question: {question}

Please provide a helpful technical response based on the context above.""")
        ])
    
    def process(self, question: str, chat_history: List[Dict[str, str]] = None) -> str:
        """Process a technical question using Pure RAG."""
        # Retrieve relevant context (RAG)
        context = self._retrieve_context(question)
        
        prompt = self._create_prompt()
        
        chain = (
            RunnablePassthrough()
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        result = chain.invoke({
            "context": context,
            "question": question
        })
        
        return result

