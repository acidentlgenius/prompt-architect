import os
import httpx
from abc import ABC, abstractmethod
from typing import Optional

class LLMBackend(ABC):
    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate response from the LLM."""
        pass

class LocalBackend(LLMBackend):
    def __init__(self, base_url: str = "http://localhost:11434/v1", model: str = "llama3"):
        self.base_url = base_url
        self.model = model
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        # Assumes OpenAI-compatible endpoint (Ollama supports this at /v1)
        # Or standard generate endpoint
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False
        }
        try:
            response = await self.client.post("/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error contacting Local LLM: {str(e)}"

class CloudBackend(LLMBackend):
    def __init__(self, api_key: str, base_url: str, model: str):
        self.client = httpx.AsyncClient(
            base_url=base_url, 
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30.0
        )
        self.model = model

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        try:
            response = await self.client.post("/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error contacting Cloud LLM: {str(e)}"

def get_backend() -> LLMBackend:
    mode = os.getenv("PROMPT_ARCHITECT_BACKEND", "local").lower()
    
    if mode == "cloud":
        return CloudBackend(
            api_key=os.getenv("PROMPT_ARCHITECT_API_KEY", ""),
            base_url=os.getenv("PROMPT_ARCHITECT_API_URL", "https://api.groq.com/openai/v1"), # Default to Groq for speed
            model=os.getenv("PROMPT_ARCHITECT_MODEL", "llama3-70b-8192")
        )
    else:
        return LocalBackend(
            base_url=os.getenv("PROMPT_ARCHITECT_LOCAL_URL", "http://localhost:11434/v1"),
            model=os.getenv("PROMPT_ARCHITECT_MODEL", "llama3")
        )
