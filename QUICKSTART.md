# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites
- Python 3.9+
- Node.js 18+
- OpenAI API key

## Step 1: Install Backend Dependencies

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

## Step 2: Configure API Keys

Create `backend/.env`:
```env
OPENAI_API_KEY=sk-your-key-here
```

## Step 3: Ingest Data

```bash
python run_ingest.py
```

## Step 4: Start Backend

```bash
python run_backend.py
```

Backend runs on http://localhost:8000

## Step 5: Start Frontend (New Terminal)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on http://localhost:3000

## Step 6: Test It!

Open http://localhost:3000 and try:
- "What are your pricing plans?" (Billing)
- "How do I set up the API?" (Technical)
- "What is your refund policy?" (Policy)

Done! 🎉

