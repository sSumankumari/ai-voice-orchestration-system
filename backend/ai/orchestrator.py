from ai.controller.qwen_controller import QwenController
from ai.conversation.llama_responder import LlamaResponder
from ai.session_state import SessionState

class Orchestrator:
    def __init__(self):
        self.controller = QwenController()
        self.responder = LlamaResponder()
        self.sessions = {}

    def handle_message(self, session_id: str, user_message: str, user_prompt: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionState()

        session = self.sessions[session_id]

        # Step 1: intent classification (for logging / future routing)
        intent = self.controller.classify_intent(user_message)

        # Step 2: generate AI response
        response = self.responder.generate(
            system_prompt=user_prompt,
            user_message=user_message,
            context=session.history
        )

        # Step 3: update memory AFTER response
        session.add_user_message(user_message)
        session.add_ai_message(response)

        return response, intent
