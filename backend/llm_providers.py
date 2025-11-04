"""LLM provider integrations for OpenAI and AWS Bedrock."""
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_aws import ChatBedrock
from langchain_core.language_models import BaseChatModel
from config import settings


def get_openai_llm(
    model_name: str = "gpt-4o-mini",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> BaseChatModel:
    """Get OpenAI LLM instance."""
    if not settings.openai_api_key:
        raise ValueError("OpenAI API key not configured")
    
    return ChatOpenAI(
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        openai_api_key=settings.openai_api_key,
    )


def get_bedrock_llm(
    model_id: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> BaseChatModel:
    """Get AWS Bedrock LLM instance."""
    if not settings.aws_access_key_id or not settings.aws_secret_access_key:
        raise ValueError("AWS credentials not configured")
    
    model_id = model_id or settings.bedrock_model_id
    
    return ChatBedrock(
        model_id=model_id,
        temperature=temperature,
        max_tokens=max_tokens,
        credentials_profile_name=None,
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )


def get_router_llm() -> BaseChatModel:
    """Get LLM for routing decisions (cost-effective, fast)."""
    # Use Bedrock for routing (fast and cost-effective)
    try:
        return get_bedrock_llm(temperature=0.1, max_tokens=100)
    except Exception:
        # Fallback to OpenAI if Bedrock not available
        return get_openai_llm(model_name="gpt-4o-mini", temperature=0.1, max_tokens=100)


def get_generator_llm() -> BaseChatModel:
    """Get LLM for response generation (high quality)."""
    # Use OpenAI for high-quality responses
    return get_openai_llm(model_name="gpt-4o-mini", temperature=0.7)

