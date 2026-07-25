# TrustLens AI Deployment & Infrastructure Guide

**Project Name:** TrustLens AI  
**Tagline:** Detect. Explain. Protect.  
**Author:** Infrastructure & DevOps Lead  
**Date:** July 25, 2026  
**Document Status:** Production Deployment Standard  

---

## 1. Overview & Architecture Requirements

TrustLens AI is deployed as a two-tier microservices architecture consisting of:
1. **Frontend Web Application:** Next.js 16 (Node.js runtime or Vercel static/SSR deployment).
2. **Backend Microservice:** FastAPI Python server running behind Uvicorn and Nginx reverse proxy.
3. **Database Layer:** MongoDB database instance.

---

## 2. Infrastructure Prerequisites

| Component | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **CPU** | 2 vCPU | 4 vCPU |
| **RAM** | 4 GB | 8 GB |
| **Storage** | 20 GB SSD | 50 GB NVMe SSD |
| **OS** | Ubuntu 22.04 LTS / Debian 12 | Ubuntu 24.04 LTS |
| **Runtime** | Docker v24.0+, Node.js 18+, Python 3.10+ | Docker v26.0+ |

---

## 3. Containerized Deployment via Docker Compose (Recommended)

### 3.1 Production `docker-compose.yml` Configuration

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:7.0
    container_name: trustlens_mongodb
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: trustlens_admin
      MONGO_INITDB_ROOT_PASSWORD: SecurePassword123!
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: trustlens_backend
    restart: always
    environment:
      - PORT=8000
      - MONGODB_URI=mongodb://trustlens_admin:SecurePassword123!@mongodb:27017/trustlens_db?authSource=admin
      - LOG_LEVEL=info
    ports:
      - "8000:8000"
    depends_on:
      - mongodb

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: trustlens_frontend
    restart: always
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  mongo_data:
```

### 3.2 Backend Dockerfile (`backend/Dockerfile`)

```dockerfile
FROM python:3.11-slim

# Install system dependencies including Tesseract OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    tesseract-ocr-eng \
    tesseract-ocr-hin \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 3.3 Launching the Stack

```bash
# Clone repository
git clone https://github.com/saloni-cmyk123/Trust-Lens-AI.git
cd Trust-Lens-AI

# Build and launch containers in background
docker compose up -d --build

# Verify container status
docker compose ps
```

---

## 4. Manual Host Deployment (Bare Metal / Ubuntu VM)

### 4.1 Installing System Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv tesseract-ocr tesseract-ocr-hin nginx git
```

### 4.2 Backend Setup & Systemd Service

1. **Setup Directory:**
   ```bash
   cd /var/www
   sudo git clone https://github.com/saloni-cmyk123/Trust-Lens-AI.git
   sudo chown -R $USER:$USER Trust-Lens-AI
   cd Trust-Lens-AI/backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Create Systemd Service (`/etc/systemd/system/trustlens-backend.service`):**
   ```ini
   [Unit]
   Description=TrustLens AI FastAPI Service
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/var/www/Trust-Lens-AI/backend
   ExecStart=/var/www/Trust-Lens-AI/backend/venv/bin/uvicorn app:app --host 127.0.0.1 --port 8000 --workers 4
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable & Start Service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable trustlens-backend
   sudo systemctl start trustlens-backend
   ```

---

## 5. Cloud Platform Deployment (Vercel + Render / AWS)

### 5.1 Frontend on Vercel
1. Connect GitHub repository `saloni-cmyk123/Trust-Lens-AI` to Vercel dashboard.
2. Set Root Directory to `frontend`.
3. Configure Environment Variable:
   `NEXT_PUBLIC_API_URL` = `https://trustlens-api.onrender.com`
4. Click **Deploy**.

### 5.2 Backend on Render / AWS EC2
1. Create new Web Service on Render linked to `backend/`.
2. Environment: `Python 3`.
3. Build Command: `pip install -r requirements.txt`.
4. Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`.

---

## 6. Environment Variables Reference

| Variable Name | Required | Default Value | Description |
| :--- | :---: | :--- | :--- |
| `PORT` | No | `8000` | Port for FastAPI server |
| `MONGODB_URI` | Yes | `mongodb://localhost:27017/trustlens` | Database connection string |
| `NEXT_PUBLIC_API_URL` | Yes | `http://localhost:8000` | Backend API URL accessed by frontend |
| `LOG_LEVEL` | No | `info` | System log output level (`debug`/`info`/`error`) |

---

*Deployment Guide certified by Infrastructure Lead.*
