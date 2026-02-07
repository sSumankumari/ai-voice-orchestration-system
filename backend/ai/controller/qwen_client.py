import requests

OLLAMA_API_BASE = "http://localhost:11434/v1"

def qwen_infer(prompt: str) -> str:
    payload = {
        "model": "qwen2.5:7b",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a strict intent classifier. "
                    "Return ONLY one category from this list:\n"
                    "medical, nutrition, finance, legal, research, interview, general"
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0
    }

    response = requests.post(
        f"{OLLAMA_API_BASE}/chat/completions",
        json=payload,
        timeout=60
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip().lower()
