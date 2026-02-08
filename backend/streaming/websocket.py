from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import uuid
import logging
import requests
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from ai.orchestrator import Orchestrator

router = APIRouter()
logger = logging.getLogger(__name__)

DJANGO_API_BASE = "http://127.0.0.1:8000/api"


def fetch_agent_config(agent_id: int):
    """
    Fetch agent configuration from Django API using agent_id.
    """
    try:
        response = requests.get(
            f"{DJANGO_API_BASE}/agents/{agent_id}/",
            timeout=5
        )

        if response.status_code == 404:
            logger.warning(f"Agent {agent_id} not found")
            return None

        if response.status_code != 200:
            logger.error(f"Django API returned status {response.status_code}")
            return None

        data = response.json()

        if "category" not in data or "system_prompt" not in data:
            logger.error(f"Agent {agent_id} missing required fields")
            return None

        return {
            "category": data["category"],
            "system_prompt": data["system_prompt"],
        }

    except requests.exceptions.Timeout:
        logger.error(f"Timeout fetching agent {agent_id}")
        return None
    except Exception as e:
        logger.error(f"Error fetching agent {agent_id}: {e}")
        return None


@router.websocket("/ws/chat/{agent_id}")
async def websocket_chat(websocket: WebSocket, agent_id: int):
    await websocket.accept()
    session_id = str(uuid.uuid4())

    logger.info(f"WebSocket connection established for agent {agent_id}, session {session_id}")

    # Fetch agent configuration
    agent_config = fetch_agent_config(agent_id)

    if not agent_config:
        await websocket.send_json({
            "type": "error",
            "message": "Agent not found or unavailable"
        })
        await websocket.close()
        return

    # Send connection confirmation with category
    await websocket.send_json({
        "type": "connected",
        "session_id": session_id,
        "category": agent_config["category"],
        "message": f"Connected to {agent_config['category']} agent"
    })

    orchestrator = Orchestrator()

    try:
        while True:
            # Receive message from client
            user_message = await websocket.receive_text()
            logger.info(f"Received message in session {session_id}: {user_message}")

            # Process with orchestrator - Enhanced format
            result = orchestrator.handle_message(
                session_id=session_id,
                user_message=user_message,
                user_prompt=agent_config["system_prompt"],
                agent_category=agent_config["category"]
            )

            # Send enhanced response to client
            await websocket.send_json({
                "type": "response",
                "message": result["response"],
                "intent": result["intent"],
                "metadata": result["metadata"]
            })

            logger.info(f"Sent response for session {session_id}")

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        logger.error(f"Error in WebSocket handler: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": "An error occurred while processing your message"
            })
        except:
            pass