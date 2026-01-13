from .backend import get_backend
from .templates import SYSTEM_PROMPT_ENHANCER, SYSTEM_PROMPT_ANALYZER
import json

class PromptEnhancer:
    def __init__(self):
        self.backend = get_backend()

    async def enhance_prompt(self, raw_prompt: str, context_files: list[str] = []) -> str:
        """
        Rewrites the raw prompt into a structured format.
        """
        user_message = f"RAW PROMPT:\n{raw_prompt}\n\n"
        if context_files:
            user_message += f"CONTEXT FILES:\n{', '.join(context_files)}\n"
        
        return await self.backend.generate(SYSTEM_PROMPT_ENHANCER, user_message)

    async def analyze_complexity(self, raw_prompt: str) -> dict:
        """
        Returns JSON analysis of the prompt.
        """
        response = await self.backend.generate(SYSTEM_PROMPT_ANALYZER, raw_prompt)
        try:
            # simple cleanup for markdown code blocks if any
            clean_response = response.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_response)
        except:
            return {
                "complexity": 0, 
                "tokens": "Unknown", 
                "suggestions": ["Could not parse analysis output."],
                "raw": response
            }
