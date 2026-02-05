from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ai.orchestrator import Orchestrator

router = APIRouter()

# One orchestrator per connection (important for session memory)
@router.websocket("/ws/chat/{agent_id}")
async def chat_websocket(websocket: WebSocket, agent_id: int):
    await websocket.accept()

    orchestrator = Orchestrator()

    try:
        while True:
            # Receive message from client
            user_message = await websocket.receive_text()

            # Process message via agentic AI core
            response = orchestrator.handle_message(user_message)

            # Send response back to client
            await websocket.send_text(response)

    except WebSocketDisconnect:
        print(f"Client disconnected (agent_id={agent_id})")
