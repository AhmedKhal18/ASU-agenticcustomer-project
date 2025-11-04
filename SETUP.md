# Setup Guide

This guide will walk you through setting up and testing the Customer Service AI Agent project step by step.

## Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] OpenAI API key (required)
- [ ] AWS account with Bedrock access (optional)

## Step 1: Clone and Navigate

```bash
cd ASU-AGENTIC-CUSTOMER-AGENT-2
```

## Step 2: Backend Setup

### 2.1 Create Virtual Environment

```bash
python -m venv venv
```

### 2.2 Activate Virtual Environment

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.4 Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cd backend
```

Create `.env` file with:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
CHROMA_DB_PATH=./chroma_db
CHROMA_COLLECTION_NAME=customer_service_kb
API_HOST=0.0.0.0
API_PORT=8000
```

**Note**: You only need `OPENAI_API_KEY` for basic functionality. AWS credentials are optional.

### 2.5 Ingest Data

Run the data ingestion script to process documents and create vector embeddings:

```bash
python ingest_data.py
```

Expected output:
```
Starting data ingestion pipeline...
Loaded X total documents
Categorized documents:
  - Billing: X
  - Technical: X
  - Policy: X
✓ Data ingestion complete!
```

### 2.6 Test the Backend (Optional)

Run the test script to verify all agents are working:

```bash
python test_agents.py
```

### 2.7 Start the Backend Server

```bash
python main.py
```

Or using uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Keep this terminal open!**

## Step 3: Frontend Setup

### 3.1 Open a New Terminal

Open a new terminal window/tab (keep backend running).

### 3.2 Navigate to Frontend

```bash
cd frontend
```

### 3.3 Install Dependencies

```bash
npm install
```

This may take a few minutes.

### 3.4 Start the Frontend

```bash
npm run dev
```

You should see:
```
- ready started server on 0.0.0.0:3000
```

### 3.5 Open the Application

Open your browser and navigate to:
```
http://localhost:3000
```

## Step 4: Testing

### Test 1: Health Check

Open a new terminal and run:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy"}
```

### Test 2: API Chat Endpoint

```bash
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"message\": \"What are your pricing plans?\"}"
```

### Test 3: Frontend Chat

1. Open http://localhost:3000 in your browser
2. Type a message in the chat input
3. Press Enter or click Send
4. Wait for the AI response

### Test Different Agent Types

Try these queries to test different agents:

**Billing Agent:**
- "What are your pricing plans?"
- "How do I get my invoice?"
- "What payment methods do you accept?"

**Technical Agent:**
- "How do I set up the API?"
- "I'm having trouble connecting"
- "What are the system requirements?"

**Policy Agent:**
- "What is your refund policy?"
- "What data do you collect?"
- "How do you handle GDPR compliance?"

## Troubleshooting

### Issue: Import Errors

**Solution**: Make sure you're running commands from the correct directory:
- Backend scripts: Run from `backend/` directory
- Frontend: Run from `frontend/` directory

### Issue: ChromaDB Not Found

**Solution**: Run the data ingestion script:
```bash
cd backend
python ingest_data.py
```

### Issue: API Key Not Found

**Solution**: 
1. Check that `.env` file exists in `backend/` directory
2. Verify the API key is correct
3. Restart the backend server after adding/changing the `.env` file

### Issue: Frontend Can't Connect to Backend

**Solution**:
1. Verify backend is running on port 8000
2. Check browser console for errors
3. Verify CORS settings in `backend/main.py`

### Issue: Module Not Found

**Solution**: 
1. Ensure virtual environment is activated
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check that you're in the correct directory

## Next Steps

1. ✅ Verify all agents are working
2. ✅ Test different query types
3. ✅ Customize prompts in agent files
4. ✅ Add more documents to `data/` directory
5. ✅ Customize the frontend UI

## Project Structure Reminder

```
ASU-AGENTIC-CUSTOMER-AGENT-2/
├── backend/          # Python FastAPI backend
│   ├── agents/      # Agent implementations
│   ├── data/        # Data ingestion
│   └── main.py      # FastAPI app
├── frontend/        # Next.js frontend
│   └── app/         # React components
└── data/            # Source documents
```

## Support

If you encounter issues:
1. Check the error messages carefully
2. Verify all prerequisites are installed
3. Ensure environment variables are set correctly
4. Review the README.md for detailed information

Good luck! 🚀

