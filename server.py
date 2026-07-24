from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn
import threading
import time
import webbrowser
import sys
import os

from backend.main import app as api_app

main_app = FastAPI(title="Travel Agent Pro", version="2.0.0")

main_app.mount("/api", api_app)

@main_app.get("/")
async def read_root():
    file_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)

@main_app.get("/api/docs")
async def api_docs():
    return FileResponse(os.path.join(os.path.dirname(__file__), "backend", "static", "api-docs.html"))

def run_server():
    uvicorn.run(main_app, host="0.0.0.0", port=8080)

def open_browser():
    time.sleep(3)
    webbrowser.open("http://localhost:8080")

if __name__ == "__main__":
    print("=" * 60)
    print("  Travel Agent Pro v2.0")
    print("  Your Personal Travel Assistant")
    print("=" * 60)
    print(f"  Frontend: http://localhost:8080")
    print(f"  API:      http://localhost:8080/api/v1")
    print(f"  Docs:     http://localhost:8080/api/docs")
    print("=" * 60)
    print("  Starting server...")

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    open_browser()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n  Server stopped. Goodbye!")
        sys.exit(0)
