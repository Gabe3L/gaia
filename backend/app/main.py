import os
from pathlib import Path
from queue import Queue
from threading import Event

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, BackgroundTasks
from backend.app.processor import Gaia, ThreadManager

app = FastAPI()

gaia = Gaia()
thread_manager = ThreadManager(gaia)

stop_event = Event()
speech_queue = Queue()
command_queue = Queue()

frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend'))

app.mount("/static", StaticFiles(directory=frontend_path), name="static")
html_path = Path(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'frontend', 'html')

@app.post("/start-thread/{thread_name}")
async def start_named_thread(thread_name: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(thread_manager.start_thread, thread_name, speech_queue, command_queue)
    return {"message": f"Started thread: {thread_name}"}

@app.post("/stop-thread/{thread_name}")
async def stop_named_thread(thread_name: str):
    thread_manager.stop_thread(thread_name)
    return {"message": f"Stopped thread: {thread_name}"}

@app.get("/")
def read_root():
    return FileResponse(html_path / "home.html")