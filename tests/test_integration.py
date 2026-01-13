import asyncio
import os
from dotenv import load_dotenv
import sys

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.backend import get_backend

async def test_backend():
    load_dotenv()
    backend = get_backend()
    
    print(f"Testing Backend: {backend.__class__.__name__}")
    print(f"Model: {backend.model}")
    
    # We expect CloudBackend if configured correctly
    if backend.__class__.__name__ != "CloudBackend":
        print("WARNING: Not using CloudBackend. Check PROMPT_ARCHITECT_BACKEND env var.")
    
    try:
        response = await backend.generate(
            system_prompt="You are a helpful assistant.", 
            user_prompt="Say 'Hello Gemini' if you can hear me."
        )
        print("\n--- Response from LLM ---")
        print(response)
        print("-------------------------")
        
        if "Hello" in response or "Gemini" in response:
            print("SUCCESS: Connection verified.")
        else:
            print("WARNING: Unexpected response.")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test_backend())
