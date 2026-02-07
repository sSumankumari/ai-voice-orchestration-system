import os
import requests

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_BASE = "https://api.groq.com/openai/v1"


def whisper_transcribe(audio_bytes: bytes) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    files = {
        "file": ("audio.wav", audio_bytes)
    }

    data = {
        "model": "whisper-large-v3"
    }

    response = requests.post(
        f"{GROQ_API_BASE}/audio/transcriptions",
        headers=headers,
        files=files,
        data=data,
        timeout=60
    )

    response.raise_for_status()
    return response.json()["text"]
