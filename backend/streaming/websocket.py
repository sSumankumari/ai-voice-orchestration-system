from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import requests
import uuid
import json
import traceback

from ai.orchestrator import Orchestrator

router = APIRouter()

# Django REST API base URL
DJANGO_API_BASE = "http://127.0.0.1:8000/api"

def fetch_agent_config(agent_id: int):
    """
    Fetch agent configuration from Django API using agent_id.
    """
    try:
        response = requests.get(f"{DJANGO_API_BASE}/agents/{agent_id}/", timeout=5)
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        return {
            "category": data["category"],
            "system_prompt": data["system_prompt"],
        }
    except requests.RequestException as e:
        print(f"Error fetching agent config: {e}")
        return None

@router.websocket("/ws/chat/{agent_id}")
async def chat_websocket(websocket: WebSocket, agent_id: int):
    await websocket.accept()

    # Fetch agent configuration from Django
    agent_config = fetch_agent_config(agent_id)

    if not agent_config:
        await websocket.send_json({
            "type": "error",
            "message": "Invalid agent ID. Please select a valid agent."
        })
        await websocket.close()
        return

    # Create orchestrator (one per WebSocket connection)
    orchestrator = Orchestrator()
    
    # Generate unique session ID for this WebSocket connection
    session_id = str(uuid.uuid4())

    try:
        # Send connection success message
        await websocket.send_json({
            "type": "connected",
            "session_id": session_id,
            "agent_id": agent_id,
            "category": agent_config["category"]
        })
        
        while True:
            # Receive message from client
            user_message = await websocket.receive_text()

            try:
                # Process via agentic AI core
                response, intent = orchestrator.handle_message(
                    session_id=session_id,
                    user_message=user_message,
                    user_prompt=agent_config["system_prompt"]
                )

                # Send AI response back to client
                await websocket.send_json({
                    "type": "response",
                    "message": response,
                    "intent": intent
                })
                
                print(f"[Session: {session_id}] Intent: {intent}")

            except Exception as e:
                print(f"Error processing message: {e}")
                traceback.print_exc()
                await websocket.send_json({
                    "type": "error",
                    "message": "Sorry, I encountered an error processing your message."
                })

    except WebSocketDisconnect:
        print(f"Client disconnected (agent_id={agent_id}, session={session_id})")
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()