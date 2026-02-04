from ai.agent_prompts import AGENT_PROMPTS

class ResponderAgent:
    """
    Conversational agent powered by Gemini LLM.
    """

    def __init__(self, llm_client):
        self.llm = llm_client

    def respond(self, user_message: str, category: str, context: list) -> str:
        system_prompt = AGENT_PROMPTS.get(category, AGENT_PROMPTS["general"])

        messages = [
            {"role": "system", "content": system_prompt}
        ]

        for msg in context:
            messages.append(msg)

        messages.append({"role": "user", "content": user_message})

        return self.llm.generate(messages)
