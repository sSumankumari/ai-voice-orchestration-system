from typing import List, Dict

class SessionState:
    """
    Maintains conversation memory per session.
    """

    def __init__(self, max_history: int = 10):
        self.history: List[Dict[str, str]] = []
        self.max_history = max_history

    def add_user_message(self, message: str):
        self._add_message("user", message)

    def add_ai_message(self, message: str):
        self._add_message("assistant", message)

    def _add_message(self, role: str, content: str):
        self.history.append({
            "role": role,
            "content": content
        })

        # Keep bounded memory
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def clear(self):
        self.history = []
