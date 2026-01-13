import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enhancer import PromptEnhancer
from src.backend import get_backend

def test_instantiation():
    try:
        backend = get_backend()
        assert backend is not None
        print("Backend instantiated successfully:", backend.__class__.__name__)
        
        enhancer = PromptEnhancer()
        assert enhancer is not None
        print("Enhancer instantiated successfully")
    except Exception as e:
        print(f"FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_instantiation()
