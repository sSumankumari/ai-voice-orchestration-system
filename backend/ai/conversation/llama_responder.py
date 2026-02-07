from ai.conversation.groq_conv import groq_chat

class LlamaResponder:
    MODEL_NAME = "llama-3.1-8b-instant"

    def generate(self, system_prompt: str, user_message: str, context: list) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
        ]

        # add conversation history
        for msg in context:
            messages.append(msg)

        # add current user message
        messages.append({"role": "user", "content": user_message})

        return groq_chat(self.MODEL_NAME, messages)
