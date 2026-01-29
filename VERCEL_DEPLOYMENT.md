# Deploying My Personal Agent to Vercel

This guide will help you deploy both the React frontend and FastAPI backend to Vercel.

## 📋 Prerequisites

1. A Vercel account ([sign up here](https://vercel.com/signup))
2. GitHub account (Vercel works best with GitHub)
3. Vercel CLI installed (optional, for local testing)

## ✅ After Pushing to GitHub (version-2)

Your repo is pushed **without** API keys. To deploy and have a usable app:

1. **Frontend on Vercel**  
   - Go to [vercel.com/new](https://vercel.com/new) → Import your GitHub repo **Bannump/RAG**.  
   - **Root Directory**: set to `RAG` (or the folder that contains `frontend`).  
   - **Build**: Root = `frontend`, Build = `npm run build`, Output = `dist`, Framework = Vite.  
   - **Env**: Add `VITE_API_URL` = your backend URL (e.g. `https://your-backend.railway.app/api`).  
   - Deploy. No API key is needed in Vercel for the frontend.

2. **Backend (API key lives here)**  
   - Deploy backend to **Railway** (or Vercel serverless) as in Option 2 below.  
   - In Railway (or Vercel) **Environment Variables**, add:  
     `OPENAI_API_KEY`, `SECRET_KEY`, and any others from `env.example`.  
   - Never put these in Git; the app reads them from the host’s env.

3. **Connect frontend to backend**  
   - Set Vercel env var `VITE_API_URL` to your backend base URL (e.g. `https://your-app.railway.app/api`), then redeploy the frontend.

## 🚀 Quick Deployment

### Option 1: Deploy via Vercel Dashboard (Recommended for Frontend)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Import Project on Vercel**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your GitHub repository
   - Select the `RAG` directory as the root
   - Vercel will auto-detect Vite/React

3. **Configure Build Settings**
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Framework Preset**: Vite

4. **Add Environment Variables**
   - In Vercel dashboard, go to Project Settings → Environment Variables
   - Add:
     ```
     VITE_API_URL=https://your-backend-url.vercel.app/api
     ```

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Your frontend will be live!

### Option 2: Deploy Backend Separately (Recommended)

Since FastAPI on Vercel requires serverless configuration, we recommend deploying the backend separately:

#### Deploy Backend to Railway (Recommended)

1. **Sign up at [railway.app](https://railway.app)**
2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
3. **Configure Service**
   - Root Directory: `backend`
   - Build Command: (leave empty, Railway auto-detects)
   - Start Command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
4. **Add Environment Variables**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `ANTHROPIC_API_KEY`: Your Anthropic API key (optional)
   - `SECRET_KEY`: Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
   - `DEFAULT_LLM_PROVIDER`: `openai`
   - `DEFAULT_MODEL`: `gpt-4o`
   - `EMBEDDING_MODEL`: `text-embedding-3-small`
   - `VECTOR_DB_PATH`: `/tmp/vector_db`
   - `DATA_DIR`: `/tmp/data`
   - `UPLOADS_DIR`: `/tmp/data/uploads`
   - `OUTPUT_DIR`: `/tmp/data/outputs`
5. **Deploy**
   - Railway will auto-deploy
   - Copy the deployed URL (e.g., `https://your-app.railway.app`)

#### Update Frontend to Use Backend URL

1. In Vercel, update environment variable:
   ```
   VITE_API_URL=https://your-backend-url.railway.app/api
   ```
2. Redeploy frontend

## 🔧 Alternative: Full Vercel Deployment

If you want to deploy both frontend and backend on Vercel:

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Configure for Vercel Python

Create `api/index.py` (Vercel serverless function wrapper):

```python
from backend.api import app
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Export app for Vercel
handler = app
```

### 3. Update vercel.json

Use the `vercel.json` file in the root directory.

### 4. Deploy

```bash
vercel --prod
```

## 📝 Environment Variables Setup

### Frontend (Vercel)

```
VITE_API_URL=https://your-backend-url.railway.app/api
```

### Backend (Railway/Render)

```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key (optional)
SECRET_KEY=generate_with_secrets_token_urlsafe_32
DEFAULT_LLM_PROVIDER=openai
DEFAULT_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-small
VECTOR_DB_PATH=/tmp/vector_db
DATA_DIR=/tmp/data
UPLOADS_DIR=/tmp/data/uploads
OUTPUT_DIR=/tmp/data/outputs
DATABASE_PATH=/tmp/data/users.db
LOG_LEVEL=INFO
ENABLE_AUTH=true
ENABLE_IMAGE_ANALYSIS=true
ENABLE_RESUME_BUILDER=true
```

## 🔄 Deployment Workflow

### Recommended Setup:
1. **Frontend**: Deploy on Vercel (fast, CDN-backed)
2. **Backend**: Deploy on Railway or Render (better for Python/FastAPI)
3. **CORS**: Update backend CORS to allow your Vercel frontend URL

### Update Backend CORS

In `backend/api.py`, update CORS settings:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://your-frontend.vercel.app",  # Add your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🧪 Testing Deployment

1. **Frontend URL**: `https://your-app.vercel.app`
2. **Backend URL**: `https://your-backend.railway.app`
3. **Test API**: `https://your-backend.railway.app/api/health`

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)

## 🐛 Troubleshooting

### Frontend can't connect to backend
- Check `VITE_API_URL` environment variable
- Verify backend CORS allows your frontend URL
- Check backend is running and accessible

### Build fails on Vercel
- Check build logs in Vercel dashboard
- Verify all dependencies in `package.json`
- Check Node.js version compatibility

### Backend errors
- Check environment variables are set correctly
- Verify API keys are valid
- Check logs in Railway/Render dashboard

## 🎉 Success!

Once deployed, your app will be live at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://your-backend.railway.app/api`
