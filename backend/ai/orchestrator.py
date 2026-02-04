from ai.intent_classifier import IntentClassifier
from ai.responder import ResponderAgent
from ai.session_state import SessionState
from ai.llm_client import GeminiLLMClient


class Orchestrator:
    """
    Central agentic controller.
    """

    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.session = SessionState()
        self.llm_client = GeminiLLMClient()
        self.responder = ResponderAgent(self.llm_client)

    def handle_message(self, message: str) -> str:
        self.session.add_user_message(message)

        result = self.intent_classifier.classify(message)
        intent = result["intent"]
        category = result["category"] or "general"

        if intent == "greeting":
            response = "Hello! How can I assist you today?"

        elif intent == "farewell":
            response = "Goodbye! Feel free to return anytime."

        else:
            response = self.responder.respond(
                user_message=message,
                category=category,
                context=self.session.get_context()
            )

        self.session.add_agent_message(response)
        return response
