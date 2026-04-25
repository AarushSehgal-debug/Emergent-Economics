import requests
import json

def ask_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )
    data = response.json()
    return data["response"]

# Test it
reply = ask_ollama("You are a trader in a village. You have 5 wood and need gold. Say what you would offer in one sentence.")
print("Agent says:", reply)