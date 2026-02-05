from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import requests

from ai.orchestrator import Orchestrator

router = APIRouter()

# Django REST API base URL
DJANGO_API_BASE = "http://127.0.0.1:8000/api"

def fetch_agent_config(agent_id: int):
    """
    Fetch agent configuration from Django API using agent_id.
    """
    response = requests.get(f"{DJANGO_API_BASE}/agents/{agent_id}/")

    if response.status_code != 200:
        return None

    data = response.json()
    return {
        "category": data["category"],
        "system_prompt": data["system_prompt"],
    }

@router.websocket("/ws/chat/{agent_id}")
async def chat_websocket(websocket: WebSocket, agent_id: int):
    await websocket.accept()

    # Fetch agent configuration from Django
    agent_config = fetch_agent_config(agent_id)

    if not agent_config:
        await websocket.send_text("Invalid agent ID. Please select a valid agent.")
        await websocket.close()
        return

    # Create orchestrator (one per WebSocket connection)
    orchestrator = Orchestrator()

    # Inject system prompt from DB into responder
    orchestrator.responder.system_prompt_override = agent_config["system_prompt"]

    try:
        while True:
            # Receive message from client
            user_message = await websocket.receive_text()

            # Process via agentic AI core
            response = orchestrator.handle_message(user_message)

            # Send AI response back to client
            await websocket.send_text(response)

    except WebSocketDisconnect:
        print(f"Client disconnected (agent_id={agent_id})")
