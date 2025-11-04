"""Orchestrator Agent - Routes queries to specialized worker agents using LangGraph."""
from typing import Dict, Any, List, Literal, TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langchain_core.output_parsers import JsonOutputParser
from llm_providers import get_router_llm
from agents.policy_agent import PolicyAgent
from agents.technical_agent import TechnicalAgent
from agents.billing_agent import BillingAgent


class AgentState(TypedDict):
    """State for the agent workflow."""
    messages: List[Dict[str, str]]
    query: str
    agent_type: str
    response: str
    session_id: str


class OrchestratorAgent:
    """Orchestrator that routes queries to specialized agents."""
    
    def __init__(self):
        self.router_llm = get_router_llm()
        self.policy_agent = PolicyAgent()
        self.technical_agent = TechnicalAgent()
        self.billing_agent = BillingAgent()
        self.workflow = self._build_workflow()
    
    def _classify_query(self, query: str) -> str:
        """Classify the query to determine which agent should handle it."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a query router for a customer service system.
Analyze the user's query and determine which specialized agent should handle it.

Available agents:
1. "billing" - For questions about invoices, payments, pricing, subscriptions, billing issues
2. "technical" - For technical support, bugs, product issues, troubleshooting, feature questions
3. "policy" - For questions about Terms of Service, Privacy Policy, compliance, legal matters

Respond with ONLY the agent name (billing, technical, or policy) in JSON format:
{{"agent": "agent_name"}}"""),
            ("human", "Query: {query}")
        ])
        
        parser = JsonOutputParser()
        
        chain = prompt | self.router_llm | parser
        
        try:
            result = chain.invoke({"query": query})
            agent_type = result.get("agent", "technical").lower()
            
            # Validate agent type
            if agent_type not in ["billing", "technical", "policy"]:
                agent_type = "technical"  # Default fallback
            
            return agent_type
        except Exception as e:
            print(f"Error classifying query: {e}")
            return "technical"  # Default fallback
    
    def _route_to_agent(self, state: AgentState) -> AgentState:
        """Route the query to the appropriate agent."""
        query = state["query"]
        agent_type = self._classify_query(query)
        
        state["agent_type"] = agent_type
        return state
    
    def _handle_billing(self, state: AgentState) -> AgentState:
        """Handle billing queries."""
        query = state["query"]
        chat_history = state.get("messages", [])
        response = self.billing_agent.process(query, chat_history)
        state["response"] = response
        return state
    
    def _handle_technical(self, state: AgentState) -> AgentState:
        """Handle technical queries."""
        query = state["query"]
        chat_history = state.get("messages", [])
        response = self.technical_agent.process(query, chat_history)
        state["response"] = response
        return state
    
    def _handle_policy(self, state: AgentState) -> AgentState:
        """Handle policy queries."""
        query = state["query"]
        chat_history = state.get("messages", [])
        response = self.policy_agent.process(query, chat_history)
        state["response"] = response
        return state
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)
        
        # Add routing node
        workflow.add_node("route", self._route_to_agent)
        
        # Add agent nodes
        workflow.add_node("billing", self._handle_billing)
        workflow.add_node("technical", self._handle_technical)
        workflow.add_node("policy", self._handle_policy)
        
        # Set entry point
        workflow.set_entry_point("route")
        
        # Add conditional edges based on agent type
        workflow.add_conditional_edges(
            "route",
            lambda state: state["agent_type"],
            {
                "billing": "billing",
                "technical": "technical",
                "policy": "policy"
            }
        )
        
        # All agents end
        workflow.add_edge("billing", END)
        workflow.add_edge("technical", END)
        workflow.add_edge("policy", END)
        
        return workflow.compile()
    
    def process(self, query: str, session_id: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Process a query through the orchestrator workflow."""
        initial_state: AgentState = {
            "messages": chat_history or [],
            "query": query,
            "agent_type": "",
            "response": "",
            "session_id": session_id
        }
        
        # Run the workflow
        result = self.workflow.invoke(initial_state)
        
        return {
            "response": result["response"],
            "agent_type": result["agent_type"],
            "session_id": session_id
        }

