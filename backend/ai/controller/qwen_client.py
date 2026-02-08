import requests
import json

OLLAMA_API_BASE = "http://localhost:11434/v1"

def qwen_infer(prompt: str, extract_json: bool = False) -> str:
    """
    Call Qwen model via Ollama API.
    
    Args:
        prompt: The prompt to send
        extract_json: If True, attempt to parse JSON from response
        
    Returns:
        String response or parsed JSON dict
    """
    payload = {
        "model": "qwen2.5:1.5b",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an intelligent intent classifier. "
                    "Analyze user queries and identify their domain and purpose. "
                    "Be flexible and creative with categories."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3 if extract_json else 0  # Slight temperature for creativity
    }

    response = requests.post(
        f"{OLLAMA_API_BASE}/chat/completions",
        json=payload,
        timeout=60
    )

    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()
    
    if extract_json:
        # Try to extract JSON from response
        try:
            # Look for JSON block
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(content[start:end])
        except:
            pass
    
    return content