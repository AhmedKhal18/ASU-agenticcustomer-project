"""Policy & Compliance Agent - Pure CAG (Context Augmented Generation)."""
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from llm_providers import get_generator_llm
from vector_store import search_documents


class PolicyAgent:
    """Agent for handling policy and compliance questions using Pure CAG."""
    
    def __init__(self):
        self.llm = get_generator_llm()
        self.collection_name = f"{self._get_collection_name()}_policy"
        self.static_context = self._load_static_context()
    
    def _get_collection_name(self) -> str:
        """Get the base collection name from settings."""
        from config import settings
        return settings.chroma_collection_name
    
    def _load_static_context(self) -> str:
        """Load static policy documents into context."""
        # For Pure CAG, we load static documents upfront
        policy_docs = search_documents(
            query="terms of service privacy policy compliance",
            collection_name=self.collection_name,
            k=10
        )
        
        context = "\n\n".join([
            f"Document {i+1}:\n{doc.page_content}" 
            for i, doc in enumerate(policy_docs)
        ])
        
        return context if context else "No policy documents found."
    
    def _create_prompt(self) -> ChatPromptTemplate:
        """Create the prompt template for policy agent."""
        return ChatPromptTemplate.from_messages([
            ("system", """You are a Policy & Compliance specialist for a customer service system.
Your role is to provide accurate, consistent answers about Terms of Service, Privacy Policy, 
and compliance-related questions.

Use the provided context to answer questions. Always cite which policy document your answer 
comes from. If the question cannot be answered from the context, politely state that you 
need to consult with a legal team member.

Context:
{context}

Be concise, professional, and accurate."""),
            ("human", "{question}")
        ])
    
    def process(self, question: str, chat_history: List[Dict[str, str]] = None) -> str:
        """Process a policy question using Pure CAG."""
        # Use static context (no retrieval at query time for Pure CAG)
        prompt = self._create_prompt()
        
        chain = (
            RunnablePassthrough()
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        result = chain.invoke({
            "context": self.static_context,
            "question": question
        })
        
        return result

