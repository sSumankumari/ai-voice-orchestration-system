from fastapi import FastAPI
from fastapi.responses import JSONResponse
from streaming.websocket import router as websocket_router

app = FastAPI(
    title="AI Voice Orchestration Streaming Service",
    description="Handles real-time AI conversations via WebSocket",
    version="1.0.0"
)

# Root endpoint - Health check
@app.get("/")
async def root():
    """
    Root endpoint - Returns service information.
    """
    return {
        "service": "AI Voice Orchestration Streaming Service",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "websocket": "/ws/chat/{agent_id}",
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health"
        }
    }

# Dedicated health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "service": "streaming",
        "message": "FastAPI WebSocket service is running"
    }

# Register WebSocket routes
app.include_router(websocket_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("streaming.main:app", host="0.0.0.0", port=8001, reload=True)