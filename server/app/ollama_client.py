import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def call_ollama(prompt: str, model: str = "sqlcoder") -> str:
    """
    Sends `prompt` to Ollama and returns the model's response text.

    We request JSON formatting so that the model returns structured output.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "format": "json",
        "stream": False,
        "options": {
            "temperature": 0
        }
    }

    resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
    resp.raise_for_status()

    data = resp.json()
    return data["response"]
