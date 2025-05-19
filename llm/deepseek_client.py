import requests
import os

def call_deepseek(prompt: str, model: str = "deepseek-chat", max_tokens: int = 500) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY")  
    url = "https://api.deepseek.com/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise RuntimeError(f"DeepSeek API Error {response.status_code}: {response.text}")
