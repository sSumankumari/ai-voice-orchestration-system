from ai.controller.qwen_controller import QwenController
from ai.conversation.llama_responder import LlamaResponder
from ai.session_state import SessionState
import time

class Orchestrator:
    def __init__(self):
        self.controller = QwenController()
        self.responder = LlamaResponder()
        self.sessions = {}

    def handle_message(self, session_id: str, user_message: str, user_prompt: str, agent_category: str = None):
        """
        Handle user message with enhanced response format.
        
        Returns:
            dict with response, intent details, and metadata
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionState()

        session = self.sessions[session_id]
        start_time = time.time()

        # Step 1: Intent classification with context
        intent_data = self.controller.classify_intent(user_message, agent_category)

        # Step 2: Generate AI response
        response = self.responder.generate(
            system_prompt=user_prompt,
            user_message=user_message,
            context=session.history
        )

        # Step 3: Update memory
        session.add_user_message(user_message)
        session.add_ai_message(response)

        # Step 4: Build enhanced response
        processing_time = time.time() - start_time
        
        return {
            "response": response,
            "intent": {
                "category": intent_data["category"],
                "subcategory": intent_data["subcategory"],
                "confidence": intent_data["confidence"]
            },
            "metadata": {
                "session_id": session_id,
                "message_count": len(session.history),
                "processing_time_ms": round(processing_time * 1000, 2),
                "agent_category": agent_category
            }
        }