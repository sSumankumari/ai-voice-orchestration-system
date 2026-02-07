from fastapi import FastAPI
from streaming.websocket import router as websocket_router

app = FastAPI(
    title="AI Voice Orchestration Streaming Service",
    description="Handles real-time AI conversations via WebSocket",
    version="1.0.0"
)

# Register WebSocket routes
app.include_router(websocket_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("streaming.main:app", host="0.0.0.0", port=8001, reload=True)