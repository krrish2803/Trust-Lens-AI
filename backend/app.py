"""
TrustLens AI - FastAPI Backend Server
Main entry point for the Scam & Phishing Detection REST API.
"""

import asyncio
import logging
import time
from collections import defaultdict
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import settings
from backend.database.mongodb import db_manager
from backend.api import scan, url, message, screenshot, history, health, auth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("trustlens.app")


# ── Rate Limiter (in-memory, per-IP) ───────────────────────────────────────
_rate_store: dict[str, list[float]] = defaultdict(list)
_rate_lock = asyncio.Lock()


async def _rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    window = settings.RATE_LIMIT_WINDOW_SECONDS
    max_requests = settings.RATE_LIMIT_REQUESTS

    async with _rate_lock:
        timestamps = _rate_store[client_ip]
        _rate_store[client_ip] = [t for t in timestamps if now - t < window]
        if len(_rate_store[client_ip]) >= max_requests:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded. Please try again later."},
            )
        _rate_store[client_ip].append(now)

    return await call_next(request)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing TrustLens AI FastAPI Backend...")
    await db_manager.connect()
    yield
    logger.info("Shutting down TrustLens AI Backend...")
    await db_manager.close()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Scam & Phishing Detection Platform tailored for Indian users.",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Configure CORS — never allow wildcard with credentials
origins = [o for o in settings.ALLOWED_ORIGINS if o != "*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.middleware("http")(_rate_limit_middleware)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, (KeyboardInterrupt, SystemExit, asyncio.CancelledError)):
        raise
    logger.error(f"Unhandled exception on {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal error occurred during threat analysis."}
    )


# Include Routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, tags=["Auth"])
app.include_router(scan.router, prefix="/scan", tags=["Scanning"])
app.include_router(url.router, prefix="/scan", tags=["Scanning"])
app.include_router(message.router, prefix="/scan", tags=["Scanning"])
app.include_router(screenshot.router, prefix="/scan", tags=["Scanning"])
app.include_router(history.router, tags=["History"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
