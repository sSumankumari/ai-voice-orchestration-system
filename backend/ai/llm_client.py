import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiLLMClient:
    """
    Gemini-powered LLM client using the new google.genai SDK.
    """

    def __init__(self, model_name: str = "gemini-2.5-flash-lite"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def generate(self, messages: list) -> str:
        """
        messages: list of dicts with role & content
        """

        # Convert structured messages into a single prompt
        prompt_parts = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            prompt_parts.append(f"{role.upper()}: {content}")

        prompt = "\n".join(prompt_parts)

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        return response.text.strip()
