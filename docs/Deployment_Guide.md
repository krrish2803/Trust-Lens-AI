# TrustLens AI - Production Deployment Guide

## 1. Backend Deployment on Render

1. Create a new **Web Service** on Render.
2. Connect your GitHub repository `Trust-Lens-AI`.
3. Set **Root Directory** to `./`.
4. Set **Environment** to `Python 3`.
5. Set **Build Command**: `pip install -r requirements.txt`
6. Set **Start Command**: `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
7. Add Environment Variables:
   - `MONGODB_URI`: Your MongoDB Atlas Connection String
   - `NVIDIA_NIM_API_KEY`: Your NVIDIA NIM API Key (`nvapi-...`)
   - `ALLOWED_ORIGINS`: `https://your-frontend-domain.vercel.app`

---

## 2. Frontend Deployment on Vercel

1. Import your GitHub repository on Vercel dashboard.
2. Select `Next.js` framework preset.
3. Set **Root Directory** to `frontend`.
4. Add Environment Variable:
   - `NEXT_PUBLIC_API_URL`: `https://trustlens-ai-backend.onrender.com`
5. Click **Deploy**.

---

## 3. Docker Deployment (Self-Hosted)

```bash
docker-compose up -d --build
```
This launches both FastAPI backend on port 8000 and MongoDB on port 27017.
