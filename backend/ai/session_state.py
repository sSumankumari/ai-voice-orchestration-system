class SessionState:
    """
        Stores conversation history per session.
    """

    def __init__(self):
        self.history = []

    def add_user_message(self, message: str):
        self.history.append({"role": "user", "content": message})

    def add_agent_message(self, message: str):
        self.history.append({"role": "assistant", "content": message})

    def get_context(self):
        return self.history[-10:]
