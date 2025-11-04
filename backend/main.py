"""FastAPI application with chat endpoint."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import AsyncIterator
import json
from models import ChatRequest, ChatResponse
from agents.orchestrator import OrchestratorAgent
from config import settings
import uuid

app = FastAPI(title="Customer Service AI Agent", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Next.js default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = OrchestratorAgent()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Customer Service AI Agent API"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint that processes user messages through the orchestrator."""
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Convert chat history format if provided
        chat_history = None
        if request.chat_history:
            chat_history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.chat_history
            ]
        
        # Process through orchestrator
        result = orchestrator.process(
            query=request.message,
            session_id=session_id,
            chat_history=chat_history
        )
        
        return ChatResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


async def stream_chat_response(message: str, session_id: str, chat_history: list = None) -> AsyncIterator[str]:
    """Stream chat response token by token."""
    try:
        # Process through orchestrator (non-streaming for now)
        result = orchestrator.process(
            query=message,
            session_id=session_id,
            chat_history=chat_history
        )
        
        # Stream the response word by word (simulated streaming)
        response = result["response"]
        words = response.split()
        
        for word in words:
            chunk = {
                "token": word + " ",
                "agent_type": result["agent_type"],
                "done": False
            }
            yield f"data: {json.dumps(chunk)}\n\n"
        
        # Send final chunk
        final_chunk = {
            "token": "",
            "agent_type": result["agent_type"],
            "done": True
        }
        yield f"data: {json.dumps(final_chunk)}\n\n"
    
    except Exception as e:
        error_chunk = {
            "error": str(e),
            "done": True
        }
        yield f"data: {json.dumps(error_chunk)}\n\n"


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint."""
    session_id = request.session_id or str(uuid.uuid4())
    
    chat_history = None
    if request.chat_history:
        chat_history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.chat_history
        ]
    
    return StreamingResponse(
        stream_chat_response(request.message, session_id, chat_history),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )

