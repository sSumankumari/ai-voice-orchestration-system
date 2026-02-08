from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import requests
import uuid
import json
import traceback
import logging

from ai.orchestrator import Orchestrator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Django REST API base URL
DJANGO_API_BASE = "http://127.0.0.1:8000/api"


def fetch_agent_config(agent_id: int):
    """
    Fetch agent configuration from Django API using agent_id.

    Args:
        agent_id: ID of the agent to fetch

    Returns:
        dict: Agent configuration with category and system_prompt
        None: If agent not found or error occurs
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

        # Validate required fields
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

    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Django API. Is it running on port 8000?")
        return None

    except requests.RequestException as e:
        logger.error(f"Error fetching agent config: {e}")
        return None

    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"Invalid response format from Django API: {e}")
        return None


@router.websocket("/ws/chat/{agent_id}")
async def chat_websocket(websocket: WebSocket, agent_id: int):
    """
    WebSocket endpoint for real-time AI chat.

    Args:
        websocket: WebSocket connection
        agent_id: ID of the agent to use for conversation
    """
    await websocket.accept()
    session_id = str(uuid.uuid4())

    logger.info(f"WebSocket connection accepted for agent {agent_id}")

    # Fetch agent configuration from Django
    agent_config = fetch_agent_config(agent_id)

    if not agent_config:
        error_message = {
            "type": "error",
            "message": f"Invalid agent ID: {agent_id}. Please select a valid agent from the Agents API.",
            "code": "INVALID_AGENT_ID"
        }
        logger.warning(f"Rejecting connection - {error_message['message']}")
        await websocket.send_json(error_message)
        await websocket.close(code=1008)  # Policy violation
        return

    # Create orchestrator (one per WebSocket connection)
    try:
        orchestrator = Orchestrator()
    except Exception as e:
        logger.error(f"Failed to create orchestrator: {e}")
        await websocket.send_json({
            "type": "error",
            "message": "Failed to initialize AI service. Please check if Ollama is running.",
            "code": "ORCHESTRATOR_INIT_FAILED"
        })
        await websocket.close(code=1011)  # Internal error
        return

    # Generate unique session ID for this WebSocket connection
    logger.info(f"Session {session_id} started for agent {agent_id}")

    try:
        # Send connection success message
        await websocket.send_json({
            "type": "connected",
            "session_id": session_id,
            "agent_id": agent_id,
            "category": agent_config["category"],
            "message": f"Connected to {agent_config['category']} agent. You can start chatting!"
        })

        while True:
            # Receive message from client
            user_message = await websocket.receive_text()

            # Validate message
            if not user_message or not user_message.strip():
                await websocket.send_json({
                    "type": "error",
                    "message": "Empty message received. Please send a valid message.",
                    "code": "EMPTY_MESSAGE"
                })
                continue

            logger.info(f"[Session {session_id}] Received: {user_message[:50]}...")

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
                    "intent": intent,
                    "timestamp": str(uuid.uuid4())  # Or use actual timestamp
                })

                logger.info(f"[Session {session_id}] Intent: {intent}")

            except RuntimeError as e:
                # Handle Ollama/AI service errors specifically
                error_msg = str(e)
                logger.error(f"Runtime error in session {session_id}: {error_msg}")

                await websocket.send_json({
                    "type": "error",
                    "message": f"AI service error: {error_msg}",
                    "code": "AI_SERVICE_ERROR",
                    "details": "Please ensure Ollama is running with the correct model."
                })

            except Exception as e:
                logger.error(f"Error processing message in session {session_id}: {e}")
                traceback.print_exc()

                await websocket.send_json({
                    "type": "error",
                    "message": "Sorry, I encountered an error processing your message. Please try again.",
                    "code": "PROCESSING_ERROR"
                })

    except WebSocketDisconnect:
        logger.info(f"Client disconnected (agent_id={agent_id}, session={session_id})")

    except Exception as e:
        logger.error(f"Unexpected error in session {session_id}: {e}")
        traceback.print_exc()

        try:
            await websocket.send_json({
                "type": "error",
                "message": "An unexpected error occurred. Connection will be closed.",
                "code": "UNEXPECTED_ERROR"
            })
        except:
            pass  # Connection might already be closed

    finally:
        logger.info(f"Session {session_id} ended")
