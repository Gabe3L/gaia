import os
import sys
import uvicorn

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    uvicorn.run(
        "backend.app.main:app",
        host="127.0.0.1",
        port=8000, 
        log_level="info"
    )
