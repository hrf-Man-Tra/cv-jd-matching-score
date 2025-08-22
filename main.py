"""
Main application entry point for CV-JD Matching API
"""
import uvicorn
import os
from dotenv import load_dotenv
from src.api.routes import app

# Load environment variables
load_dotenv()

def main():
    """
    Main function to run the FastAPI application
    """
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print("=" * 50)
    print("🚀 Starting CV-JD Matching API Server")
    print("=" * 50)
    print(f"📍 Server: http://{host}:{port}")
    print(f"📚 API Docs: http://{host}:{port}/docs")
    print(f"📋 ReDoc: http://{host}:{port}/redoc")
    print(f"🔧 Debug Mode: {debug}")
    print("=" * 50)
    
    # Run the server
    uvicorn.run(
        "src.api.routes:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if not debug else "debug"
    )

if __name__ == "__main__":
    main()