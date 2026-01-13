from mcp.server.fastmcp import FastMCP
from .enhancer import PromptEnhancer

# Initialize FastMCP which handles lifecycle and verification
mcp = FastMCP("Prompt Architect")

# Initialize logic
enhancer = PromptEnhancer()

@mcp.tool()
async def architect_prompt(raw_prompt: str, context_files: list[str] = []) -> str:
    """
    Rewrites a raw user prompt into a structured, optimized prompt for coding agents.
    Args:
        raw_prompt: The user's original, unstructured request.
        context_files: Optional list of filenames relevant to the task.
    """
    return await enhancer.enhance_prompt(raw_prompt, context_files)

@mcp.tool()
async def analyze_complexity(raw_prompt: str) -> dict:
    """
    Analyzes the complexity of a prompt and provides detailed metrics.
    Args:
        raw_prompt: The user's original request.
    """
    return await enhancer.analyze_complexity(raw_prompt)

if __name__ == "__main__":
    mcp.run()
