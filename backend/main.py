from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
load_dotenv()
from routes import planner
from models import HealthResponse



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 AI Holiday Planner API starting...")
    yield
    # Shutdown
    print("👋 AI Holiday Planner API shutting down...")


app = FastAPI(
    title="AI Holiday Planner API",
    description="An intelligent holiday planning API powered by Cerebras LLM",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint to verify API is running."""
    return HealthResponse(status="healthy", message="API is running successfully")

# Include routers
app.include_router(planner.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)