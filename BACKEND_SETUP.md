# Backend API Server Setup

## The Issue

The React frontend is trying to connect to a backend API at `http://localhost:8000/api`, but no server is running. The error `ERR_CONNECTION_REFUSED` confirms this.

## Solution

A FastAPI backend server has been created in `backend/api.py` that wraps your existing Python modules.

## Quick Start

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Start the Server

From the project root (RAG directory):

```bash
# Make sure you're in the project root with venv activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the backend server
python -m backend.api
```

Or use uvicorn directly:

```bash
uvicorn backend.api:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Verify Server is Running

The server should start and show:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

You can test it in your browser: http://localhost:8000/api/health

Should return: `{"status": "healthy"}`

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/vehicle` - Vehicle diagnostics (multipart/form-data: image, description)
- `POST /api/resume/analyze` - Resume analysis (multipart/form-data: resume, job_description)
- `POST /api/resume/build` - Resume builder (JSON body)

## Running Frontend and Backend Together

You need to run both servers:

### Terminal 1: Backend
```bash
cd RAG
source venv/bin/activate
uvicorn backend.api:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2: Frontend
```bash
cd RAG/frontend
npm run dev
```

Then access the frontend at http://localhost:3000

## CORS Configuration

The backend is configured to allow requests from:
- http://localhost:3000
- http://127.0.0.1:3000

If you deploy to different ports, update the CORS settings in `backend/api.py`.
