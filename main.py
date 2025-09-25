#!/usr/bin/env python3
"""
Main entry point for RAGAS Backend API
"""

import uvicorn
import sys
import os
from config import config

def main():
    """Run the FastAPI application"""
    try:
        # Validate configuration before starting
        config.validate()
        print("✅ Configuration validated")
        print(f"📡 Starting RAGAS API on {config.API_HOST}:{config.API_PORT}")
        print(f"📚 Default Provider: {config.DEFAULT_PROVIDER}")
        print(f"🤖 Default LLM: {config.DEFAULT_LLM_MODEL}")
        print(f"🔤 Default Embeddings: {config.DEFAULT_EMBEDDING_MODEL}")
        print("-" * 50)
        
        # Run the application
        uvicorn.run(
            "app:app",
            host=config.API_HOST,
            port=config.API_PORT,
            reload=True,  # Enable auto-reload for development
            log_level="info"
        )
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Startup Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()