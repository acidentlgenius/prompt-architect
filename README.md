# Prompt Architect

**Don't write vague prompts. Architect them properly.**

Prompt Architect is a middleware layer for your AI coding assistants (like Antigravity, Cursor, Windsurf, or Cline). Basically, it acts like a **Senior Engineer** checking your work. It takes your raw, simple requirement (e.g., "add login page") and expands it into a proper, step-by-step technical plan *before* the AI starts coding.

**Core Logic:** It bridges the gap between what you *think* you want and what the AI *needs* to know.

---

## 🚀 Quick Setup (Practical)

Follow these steps to get the server running on your local machine.

### 1. Prerequisite
You must have [`uv`](https://github.com/astral-sh/uv) installed. It is a very fast package manager for Python.
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Installation
Clone the repository and install the dependencies.
```bash
git clone https://github.com/your-repo/prompt-architect.git
cd prompt-architect
uv sync
```

### 3. Configuration
One-time setup for the environment variables.
```bash
cp .env.example .env
```
Open the `.env` file. You have two options (select one according to your requirement):

*   **Option A: Cloud Mode (Recommended)**
    *   Use this for better performance and logic.
    *   Get a free API Key from Google AI Studio (Gemini 2.5 Flash Lite) or use OpenAI/Groq keys.
    *   Set the `PROMPT_ARCHITECT_API_KEY` in the file.

*   **Option B: Local Mode (Privacy Focused)**
    *   Use this if you want to keep data on your system.
    *   Install [Ollama](https://ollama.com).
    *   Set `PROMPT_ARCHITECT_BACKEND=local`.

---

## 🔌 Usage Guide

### Scenario 1: Using with Cursor
1.  Navigate to **Settings** > **Features** > **MCP**.
2.  Click on "Add New MCP Server".
3.  Enter the following details:
    *   **Name:** `Prompt Architect`
    *   **Type:** `Command`
    *   **Command:** `uv --directory /absolute/path/to/prompt-architect run main.py`

### Scenario 2: Using with Antigravity
Add this code block to your `~/.gemini/antigravity/mcp_config.json` file:
```json
{
  "mcpServers": {
    "prompt-architect": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/prompt-architect",
        "run",
        "main.py"
      ]
    }
  }
}
```

### Scenario 3: Using with VS Code (Windsurf / Cline)
Edit your MCP configuration file (usually found at `mcp_config.json`):
```json
"prompt-architect": {
  "command": "uv",
  "args": ["--directory", "/absolute/path/to/prompt-architect", "run", "main.py"]
}
```

**How to verify:** Ask your agent, "Use the Architect tool to plan a login system." If it creates a detailed plan, the setup is successful.

---

## 🧠 Technical Concepts (Deep Dive)

This section explains the internal working mechanism for technical users.

### The Architecture
The project is built using `mcp-python`. It exposes two main tools:

1.  **`architect_prompt`**: This is the primary function. It accepts a `raw_prompt` and optional context. It uses a "Chain of Thought" process to analyze the requirement and returns a structured Markdown plan.
2.  **`analyze_complexity`**: This is a utility function. It calculates a complexity score (1-10) for the task to help you understand the risk involved.

### Backend Modes (Dual-Fuel Logic)

#### 1. Cloud Mode (Default)
This mode connects to external APIs.
*   **Provider:** Google Gemini 2.5 Flash Lite or standard OpenAI/Groq endpoints.
*   **Advantage:** High reasoning capability and low latency.
*   **Note:** Data is sent over HTTPS.

#### 2. Local Mode
This mode runs the model on your machine.
*   **Provider:** Ollama.
*   **Advantage:** Complete data privacy. No data leaves your laptop.
*   **Trade-off:** Performance depends on your hardware (RAM/GPU).

### Important Variables (`.env`)

| Variable | Meaning | Default Value |
| :--- | :--- | :--- |
| `PROMPT_ARCHITECT_BACKEND` | Switch between `cloud` and `local` | `cloud` |
| `PROMPT_ARCHITECT_API_KEY` | Your API credential | Required for cloud |
| `PROMPT_ARCHITECT_MODEL` | Specific model ID (e.g., `gemini-2.0-flash-exp`) | `gemini-2.0-flash-exp` |
| `OLLAMA_HOST` | Local server address | `http://localhost:11434` |
| `LOG_LEVEL` | Logging detail level | `INFO` |

### Testing
To verify the system integrity, run the integration tests:
```bash
uv run pytest tests/test_integration.py
```
