"""Billing Support Agent - Hybrid RAG/CAG."""
from typing import Dict, Any, List, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from llm_providers import get_generator_llm
from vector_store import search_documents


class BillingAgent:
    """Agent for handling billing questions using Hybrid RAG/CAG."""
    
    def __init__(self):
        self.llm = get_generator_llm()
        self.collection_name = f"{self._get_collection_name()}_billing"
        self.cached_policy: Optional[str] = None
        self._initial_rag_done = False
    
    def _get_collection_name(self) -> str:
        """Get the base collection name from settings."""
        from config import settings
        return settings.chroma_collection_name
    
    def _initial_rag_retrieval(self) -> str:
        """Perform initial RAG to cache static policy information."""
        if self._initial_rag_done and self.cached_policy:
            return self.cached_policy
        
        # Retrieve billing policies and pricing information
        policy_docs = search_documents(
            query="billing policy pricing subscription invoice payment terms",
            collection_name=self.collection_name,
            k=10
        )
        
        cached_content = "\n\n".join([
            f"Document {i+1}:\n{doc.page_content}" 
            for i, doc in enumerate(policy_docs)
        ])
        
        self.cached_policy = cached_content if cached_content else "No billing policy found."
        self._initial_rag_done = True
        
        return self.cached_policy
    
    def _retrieve_dynamic_context(self, question: str, k: int = 3) -> str:
        """Retrieve dynamic context relevant to the specific question."""
        docs = search_documents(question, self.collection_name, k=k)
        
        if not docs:
            return ""
        
        context = "\n\n".join([
            f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}" 
            for doc in docs
        ])
        
        return context
    
    def _create_prompt(self) -> ChatPromptTemplate:
        """Create the prompt template for billing agent."""
        return ChatPromptTemplate.from_messages([
            ("system", """You are a Billing Support specialist for a customer service system.
Your role is to help customers with billing, invoicing, pricing, and payment questions.

Use both the cached billing policy information and any dynamically retrieved context to 
provide accurate answers. The cached policy contains static information about pricing, 
subscription terms, and payment policies. The dynamic context may contain specific 
invoice details or recent updates.

Be precise with numbers, dates, and payment terms. If you cannot find the answer, 
suggest contacting the billing department directly."""),
            ("human", """Cached Billing Policy (Static):
{static_context}

Dynamic Context (if available):
{dynamic_context}

User Question: {question}

Please provide a helpful billing response based on the information above.""")
        ])
    
    def process(self, question: str, chat_history: List[Dict[str, str]] = None) -> str:
        """Process a billing question using Hybrid RAG/CAG."""
        # Get cached static policy (CAG - from initial RAG)
        static_context = self._initial_rag_retrieval()
        
        # Retrieve dynamic context for specific question (RAG)
        dynamic_context = self._retrieve_dynamic_context(question)
        
        prompt = self._create_prompt()
        
        chain = (
            RunnablePassthrough()
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        result = chain.invoke({
            "static_context": static_context,
            "dynamic_context": dynamic_context if dynamic_context else "No additional dynamic context found.",
            "question": question
        })
        
        return result

