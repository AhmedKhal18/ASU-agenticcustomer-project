"""Test script for verifying all agents are working correctly."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.orchestrator import OrchestratorAgent
from config import settings


def test_orchestrator():
    """Test the orchestrator and all agents."""
    print("=" * 60)
    print("Testing Customer Service AI Agents")
    print("=" * 60)
    
    # Check configuration
    print("\n1. Checking Configuration...")
    if not settings.openai_api_key:
        print("❌ ERROR: OPENAI_API_KEY not set")
        return False
    print("✓ OpenAI API key configured")
    
    if settings.aws_access_key_id and settings.aws_secret_access_key:
        print("✓ AWS credentials configured")
    else:
        print("⚠ AWS credentials not set (will use OpenAI fallback)")
    
    # Initialize orchestrator
    print("\n2. Initializing Orchestrator...")
    try:
        orchestrator = OrchestratorAgent()
        print("✓ Orchestrator initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing orchestrator: {e}")
        return False
    
    # Test queries for each agent type
    test_cases = [
        {
            "category": "Billing",
            "queries": [
                "What are your pricing plans?",
                "How do I get my invoice?",
                "What payment methods do you accept?",
            ]
        },
        {
            "category": "Technical",
            "queries": [
                "How do I set up the API?",
                "I'm having trouble connecting",
                "What are the system requirements?",
            ]
        },
        {
            "category": "Policy",
            "queries": [
                "What is your refund policy?",
                "What data do you collect?",
                "How do you handle GDPR compliance?",
            ]
        }
    ]
    
    print("\n3. Testing Agent Routing and Responses...")
    print("-" * 60)
    
    all_passed = True
    
    for test_case in test_cases:
        category = test_case["category"]
        queries = test_case["queries"]
        
        print(f"\n📋 Testing {category} Agent:")
        for i, query in enumerate(queries, 1):
            try:
                print(f"\n  Query {i}: {query}")
                result = orchestrator.process(
                    query=query,
                    session_id=f"test-session-{category.lower()}"
                )
                
                agent_type = result["agent_type"]
                response = result["response"]
                
                print(f"  → Routed to: {agent_type} agent")
                print(f"  → Response preview: {response[:100]}...")
                
                # Verify routing
                expected_agent = category.lower()
                if agent_type == expected_agent:
                    print(f"  ✓ Correctly routed to {agent_type} agent")
                else:
                    print(f"  ⚠ Routed to {agent_type} instead of {expected_agent}")
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests completed!")
    else:
        print("⚠ Some tests had issues. Check the errors above.")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    success = test_orchestrator()
    sys.exit(0 if success else 1)

