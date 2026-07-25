"""
TrustLens AI - FastAPI Backend Server
Main entry point for the Scam & Phishing Detection REST API.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import settings
from backend.database.mongodb import db_manager
from backend.api import scan, url, message, screenshot, history, health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("trustlens.app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect DB
    logger.info("Initializing TrustLens AI FastAPI Backend...")
    await db_manager.connect()
    yield
    # Shutdown: close DB connection
    logger.info("Shutting down TrustLens AI Backend...")
    await db_manager.close()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Scam & Phishing Detection Platform tailored for Indian users.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal error occurred during threat analysis."}
    )


# Include Routers
app.include_router(health.router, tags=["Health"])
app.include_router(scan.router, prefix="/scan", tags=["Scanning"])
app.include_router(url.router, prefix="/scan", tags=["Scanning"])
app.include_router(message.router, prefix="/scan", tags=["Scanning"])
app.include_router(screenshot.router, prefix="/scan", tags=["Scanning"])
app.include_router(history.router, tags=["History"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
