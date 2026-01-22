"""
FastAPI application main entry point.
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.database import connect_to_mongo, close_mongo_connection
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup: Connect to MongoDB
    await connect_to_mongo()
    yield
    # Shutdown: Close MongoDB connection
    await close_mongo_connection()


# Create FastAPI application instance
app = FastAPI(
    title="CHL API",
    description="FastAPI application with MongoDB integration using Motor",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to CHL API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "CHL API"
    }
