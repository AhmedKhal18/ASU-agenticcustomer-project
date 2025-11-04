"""Helper script to run the backend server."""
import os
import sys

# Change to backend directory
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
os.chdir(backend_dir)

# Add backend to path
sys.path.insert(0, backend_dir)

# Run the server
if __name__ == "__main__":
    import uvicorn
    from config import settings
    
    print("Starting Customer Service AI Backend...")
    print(f"API will be available at http://{settings.api_host}:{settings.api_port}")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )

