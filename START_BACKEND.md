# Start Backend API Server

## Problem Identified

The error `ERR_CONNECTION_REFUSED` on `:8000/api/resume/analyze` confirms that **no backend API server is running**.

## Solution

A FastAPI backend server has been created at `backend/api.py`. You need to start it.

## Quick Start

### Start the Backend Server

In your WSL terminal (make sure you're in the project root with venv activated):

```bash
# Navigate to project root
cd /mnt/c/Users/sarat/OneDrive/Documents/self_learning/RAG/RAG

# Activate virtual environment
source venv/bin/activate

# Start the backend API server
uvicorn backend.api:app --host 0.0.0.0 --port 8000 --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Verify Backend is Running

Open in browser: http://localhost:8000/api/health

Should return: `{"status": "healthy"}`

### Now Try the Frontend Again

With the backend running, try the resume analysis in your React frontend again. It should work now!

## Running Both Servers

You need **two terminals**:

**Terminal 1 - Backend:**
```bash
cd RAG
source venv/bin/activate
uvicorn backend.api:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd RAG/frontend
npm run dev
```

Then access frontend at: http://localhost:3000
