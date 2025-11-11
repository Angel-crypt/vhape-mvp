#!/usr/bin/env python3
"""
Python-based runner for Vhape Dummy API.
This script ensures proper environment setup and runs the FastAPI server.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Run the FastAPI server using uvicorn."""
    import uvicorn
    
    print("=" * 60)
    print("Starting Vhape Dummy API...")
    print("=" * 60)
    print("\nFastAPI documentation:")
    print("  - Swagger UI: http://localhost:8000/docs")
    print("  - ReDoc:     http://localhost:8000/redoc")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        uvicorn.run(
            "api_dummy.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError starting server: {e}")
        print("\nMake sure dependencies are installed:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()

