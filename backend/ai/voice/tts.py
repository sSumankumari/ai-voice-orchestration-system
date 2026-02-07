import os
import requests

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_BASE = "https://api.groq.com/openai/v1"


def whisper_tts(text: str) -> bytes:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini-tts",
        "input": text,
        "voice": "alloy"
    }

    response = requests.post(
        f"{GROQ_API_BASE}/audio/speech",
        json=payload,
        headers=headers,
        timeout=60
    )

    response.raise_for_status()
    return response.content
