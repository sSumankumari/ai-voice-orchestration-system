import os
import requests

from dotenv import load_dotenv
load_dotenv()

GROQ_API_BASE = "https://api.groq.com/openai/v1"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable not set")

def groq_chat(model: str, messages: list) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.6
    }

    response = requests.post(
        f"{GROQ_API_BASE}/chat/completions",
        json=payload,
        headers=headers,
        timeout=60
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
