# Quick Guide: Deploy to Vercel

## Step 1: Prepare Your Code

Make sure your code is committed and pushed to GitHub:

```bash
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

## Step 2: Deploy Frontend to Vercel

1. **Go to [vercel.com/new](https://vercel.com/new)**
2. **Import your GitHub repository**
3. **Configure Project**:
   - **Root Directory**: Click "Edit" → Change to `frontend`
   - **Framework Preset**: Vite (auto-detected)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **Add Environment Variable**:
   - Go to "Environment Variables"
   - Add: `VITE_API_URL` = (we'll set this after deploying backend)

5. **Click "Deploy"**

## Step 3: Deploy Backend to Railway

1. **Go to [railway.app](https://railway.app)**
2. **Sign up/Login** with GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Select your repository**
5. **Configure**:
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`

6. **Add Environment Variables** (in Railway dashboard):
   ```
   OPENAI_API_KEY=your_key_here
   SECRET_KEY=generate_with_python_c_secrets_token_urlsafe_32
   DEFAULT_MODEL=gpt-4o
   VECTOR_DB_PATH=/tmp/vector_db
   DATA_DIR=/tmp/data
   UPLOADS_DIR=/tmp/data/uploads
   OUTPUT_DIR=/tmp/data/outputs
   ```

7. **Deploy** → Copy your Railway URL (e.g., `https://your-app.railway.app`)

## Step 4: Connect Frontend to Backend

1. **In Vercel Dashboard**:
   - Go to your project → Settings → Environment Variables
   - Update `VITE_API_URL` to: `https://your-app.railway.app/api`
   - Click "Redeploy"

2. **Update Backend CORS** (in `backend/api.py`):
   - Add your Vercel URL to `allowed_origins`
   - Redeploy backend

## Step 5: Test

1. Visit your Vercel frontend URL
2. Try uploading a resume or image
3. Check browser console for any errors

## 🎉 Done!

Your app is now live on the web!

- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-backend.railway.app/api`
