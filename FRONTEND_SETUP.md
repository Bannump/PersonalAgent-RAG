# Frontend Dashboard Setup Guide

## Overview

A React-based dashboard has been created for the My Personal Agent application with a modern dark theme.

## Features

- ✅ Dark theme UI (black background)
- ✅ Dashboard with feature cards
- ✅ Vehicle Diagnostics interface
- ✅ Resume Analysis interface
- ✅ Resume Builder interface
- ✅ Responsive design
- ✅ Modern React with hooks

## Quick Start

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Start Development Server

```bash
npm run dev
```

The dashboard will be available at `http://localhost:3000`

## Backend API Setup

The frontend expects a backend API. You'll need to create API endpoints or use the existing CLI. 

### Option 1: Create FastAPI Backend (Recommended)

Create a FastAPI server to handle API requests:

```python
# backend/api.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from src.my_personal_agent.modules.vehicle_diagnostics import VehicleDiagnostics
# ... import other modules

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/vehicle")
async def diagnose_vehicle(image: UploadFile = File(...), description: str = Form("")):
    # Implementation
    pass

@app.post("/api/resume/analyze")
async def analyze_resume(resume: UploadFile = File(...), job_description: str = Form(...)):
    # Implementation
    pass

@app.post("/api/resume/build")
async def build_resume(data: dict):
    # Implementation
    pass
```

### Option 2: Use Proxy (Development Only)

For development, you can use the existing CLI through a proxy, but you'll need to create API endpoints.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.jsx          # Main dashboard
│   │   ├── VehicleDiagnostics.jsx # Vehicle diagnostics UI
│   │   ├── ResumeAnalysis.jsx     # Resume analysis UI
│   │   ├── ResumeBuilder.jsx      # Resume builder UI
│   │   └── *.css                  # Component styles
│   ├── services/
│   │   └── api.js                 # API client
│   ├── App.jsx                    # Main app component
│   ├── App.css                    # App styles
│   ├── main.jsx                   # Entry point
│   └── index.css                  # Global styles
├── public/
├── package.json
├── vite.config.js
└── README.md
```

## Build for Production

```bash
# Build
npm run build

# Preview
npm run preview
```

## Environment Variables

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000/api
```

## Next Steps

1. **Set up backend API** - Create FastAPI endpoints (or use existing CLI through API wrapper)
2. **Test the UI** - Run `npm run dev` and test each feature
3. **Customize styling** - Adjust colors, fonts, spacing as needed
4. **Deploy** - Deploy frontend (Vercel, Netlify) and backend (Render, Railway) separately

## Notes

- The frontend is ready to use but needs backend API endpoints
- All API calls are configured in `src/services/api.js`
- Dark theme is applied throughout
- Responsive design works on mobile and desktop
- Uses React Router for navigation
