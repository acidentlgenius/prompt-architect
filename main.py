import os
from dotenv import load_dotenv

# Load .env from the directory where main.py resides
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"))

from src.server import mcp

if __name__ == "__main__":
    mcp.run()
