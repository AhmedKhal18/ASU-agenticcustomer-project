# ASU Agentic Customer Agent

A sophisticated, proof-of-concept customer service application powered by a multi-agent AI system. This application demonstrates a modern, scalable architecture for handling diverse customer inquiries by routing them to specialized AI agents.

## 🎯 Project Overview

This project implements a **multi-agent customer service system** with:
- **Orchestrator Agent**: Intelligently routes queries to specialized agents
- **Billing Support Agent**: Hybrid RAG/CAG for pricing and invoice questions
- **Technical Support Agent**: Pure RAG for technical documentation
- **Policy & Compliance Agent**: Pure CAG for terms and privacy policies

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python
- **AI/LLM**: LangChain with LangGraph for agent orchestration
- **Vector Database**: ChromaDB (local persistence)
- **LLM Providers**: OpenAI (GPT-4) and AWS Bedrock (Claude 3 Haiku)

### Frontend (Next.js)
- **Framework**: Next.js 14 with React
- **Styling**: Tailwind CSS
- **Features**: Real-time chat interface with streaming support

## 📋 Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- OpenAI API key
- AWS account with Bedrock access (optional, will fallback to OpenAI)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/AhmedKhal18/ASU-agenticcustomer-project.git
cd ASU-AGENTIC-CUSTOMER-AGENT-2
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key_id_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
CHROMA_DB_PATH=./chroma_db
CHROMA_COLLECTION_NAME=customer_service_kb
API_HOST=0.0.0.0
API_PORT=8000
```

**Note**: AWS credentials are optional. The system will fallback to OpenAI if Bedrock is not configured.

### 4. Ingest Data

Run the data ingestion pipeline to process documents and create vector embeddings:

**Option 1: Using helper script (recommended)**
```bash
python run_ingest.py
```

**Option 2: Direct script**
```bash
cd backend
python ingest_data.py
```

This will:
- Load documents from the `data/` directory
- Categorize them (billing, technical, policy)
- Create vector embeddings using OpenAI
- Store them in ChromaDB

### 5. Start the Backend Server

**Option 1: Using helper script (recommended)**
```bash
python run_backend.py
```

**Option 2: Direct uvicorn**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 6. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
ASU-AGENTIC-CUSTOMER-AGENT-2/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py      # Main orchestrator agent
│   │   ├── billing_agent.py     # Billing support (Hybrid RAG/CAG)
│   │   ├── technical_agent.py   # Technical support (Pure RAG)
│   │   └── policy_agent.py      # Policy & compliance (Pure CAG)
│   ├── config.py                # Configuration settings
│   ├── ingest_data.py           # Data ingestion pipeline
│   ├── llm_providers.py         # LLM provider integrations
│   ├── main.py                  # FastAPI application
│   ├── models.py                # Pydantic models
│   └── vector_store.py          # ChromaDB utilities
├── frontend/
│   ├── app/
│   │   ├── page.tsx             # Main chat interface
│   │   ├── layout.tsx           # Root layout
│   │   └── globals.css          # Global styles
│   ├── package.json
│   └── next.config.js
├── data/
│   ├── billing/                 # Billing-related documents
│   ├── technical/               # Technical documentation
│   └── policy/                  # Policy documents
├── requirements.txt
├── run_backend.py          # Helper script to run backend
├── run_ingest.py           # Helper script to run data ingestion
├── README.md               # This file
├── SETUP.md                # Detailed setup guide
└── QUICKSTART.md           # Quick start guide
```

## 🔧 Agent Architecture

### Orchestrator Agent
- **Purpose**: Routes user queries to the appropriate specialized agent
- **LLM**: AWS Bedrock (Claude 3 Haiku) for fast, cost-effective routing
- **Method**: Classification-based routing using LangGraph

### Billing Support Agent (Hybrid RAG/CAG)
- **Purpose**: Handles billing, pricing, and invoice questions
- **Strategy**: 
  - Initial RAG to cache static policy information (CAG)
  - Dynamic RAG for query-specific context
- **LLM**: OpenAI GPT-4

### Technical Support Agent (Pure RAG)
- **Purpose**: Handles technical issues and product questions
- **Strategy**: Pure RAG - retrieves relevant docs for each query
- **LLM**: OpenAI GPT-4

### Policy & Compliance Agent (Pure CAG)
- **Purpose**: Answers questions about Terms of Service and Privacy Policy
- **Strategy**: Pure CAG - loads static documents upfront, no retrieval at query time
- **LLM**: OpenAI GPT-4

## 🧪 Testing

### Test the Backend API

```bash
# Health check
curl http://localhost:8000/health

# Chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are your pricing plans?",
    "session_id": "test-session-123"
  }'
```

### Test Different Agent Types

1. **Billing Questions**:
   - "What are your pricing plans?"
   - "How do I get my invoice?"
   - "What payment methods do you accept?"

2. **Technical Questions**:
   - "How do I set up the API?"
   - "I'm having trouble connecting to the service"
   - "What are the system requirements?"

3. **Policy Questions**:
   - "What is your refund policy?"
   - "What data do you collect?"
   - "How do you handle GDPR compliance?"

## 📊 API Endpoints

### `GET /health`
Health check endpoint.

### `POST /chat`
Main chat endpoint for processing messages.

**Request Body**:
```json
{
  "message": "What are your pricing plans?",
  "session_id": "optional-session-id",
  "chat_history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"}
  ]
}
```

**Response**:
```json
{
  "response": "We offer three pricing plans...",
  "agent_type": "billing",
  "session_id": "session-id"
}
```

### `POST /chat/stream`
Streaming chat endpoint (Server-Sent Events).

## 🔄 Data Ingestion

The data ingestion pipeline (`ingest_data.py`) processes documents from the `data/` directory:

- **Supported formats**: `.txt`, `.pdf`, `.docx`
- **Categorization**: Automatically categorizes documents by content
- **Vector storage**: Creates separate ChromaDB collections for each category

To add new documents:
1. Place them in the appropriate `data/` subdirectory
2. Run `python ingest_data.py` again

## 🎨 Frontend Features

- Clean, modern chat interface
- Real-time message display
- Agent type indicators
- Responsive design
- Streaming support (ready for future enhancements)

## 🛠️ Development

### Adding New Agents

1. Create a new agent class in `backend/agents/`
2. Implement the `process()` method
3. Add the agent to the orchestrator in `backend/agents/orchestrator.py`
4. Update the routing logic

### Customizing Prompts

Edit the prompt templates in each agent file:
- `backend/agents/billing_agent.py`
- `backend/agents/technical_agent.py`
- `backend/agents/policy_agent.py`

## 📝 Notes

- The system uses **LangGraph** for stateful agent orchestration
- **ChromaDB** provides persistent vector storage
- **Multi-provider strategy** optimizes for cost (Bedrock) and quality (OpenAI)
- The orchestrator intelligently routes queries based on content analysis

## 🐛 Troubleshooting

### ChromaDB Issues
- Ensure ChromaDB is installed: `pip install chromadb`
- Delete `chroma_db/` directory and re-run ingestion if needed

### API Key Issues
- Verify your `.env` file has correct API keys
- Check that environment variables are loaded correctly

### Import Errors
- Ensure you're running from the correct directory
- Check that all dependencies are installed

### Frontend Connection Issues
- Verify backend is running on port 8000
- Check CORS settings in `backend/main.py`

## 📚 Technologies Used

- **FastAPI**: Modern Python web framework
- **LangChain**: LLM application framework
- **LangGraph**: Agent orchestration
- **ChromaDB**: Vector database
- **OpenAI API**: GPT models
- **AWS Bedrock**: Claude models
- **Next.js**: React framework
- **Tailwind CSS**: Styling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is for educational and portfolio purposes.

## 👤 Author

Ahmed Khalil - ASU Agentic Customer Agent Project

## 🙏 Acknowledgments

- LangChain team for excellent documentation
- OpenAI for GPT models
- AWS for Bedrock service

---

**Status**: ✅ MVP Complete - Ready for testing and enhancement
