from ai.agent_prompts import AGENT_PROMPTS

class ResponderAgent:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.system_prompt_override = None

    def respond(self, user_message: str, category: str, context: list) -> str:
        system_prompt = self.system_prompt_override or AGENT_PROMPTS.get(category)

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(context)
        messages.append({"role": "user", "content": user_message})

        return self.llm.generate(messages)
