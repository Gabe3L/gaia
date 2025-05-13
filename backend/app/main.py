import os
import asyncio
from queue import Queue
from typing import List
from pathlib import Path
from threading import Event

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect

from backend.app.processor import Gaia, ThreadManager
from backend.app.apis.online import *

#####################################################################

app = FastAPI()

gaia = Gaia()
thread_manager = ThreadManager(gaia)

stop_event = Event()
speech_queue = Queue()
command_queue = Queue()

frontend_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'frontend'))

app.mount("/static", StaticFiles(directory=frontend_path), name="static")
html_path = Path(os.path.dirname(os.path.abspath(__file__)),
                 '..', '..', 'frontend', 'html')

connected_clients: List[WebSocket] = []

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

#####################################################################

@app.get("/")
def read_root():
    return FileResponse(html_path / "home.html")


@app.post("/start-thread/{thread_name}")
async def start_named_thread(thread_name: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        thread_manager.start_thread, thread_name, speech_queue, command_queue)
    return {"message": f"Started thread: {thread_name}"}


@app.post("/stop-thread/{thread_name}")
async def stop_named_thread(thread_name: str):
    thread_manager.stop_thread(thread_name)
    return {"message": f"Stopped thread: {thread_name}"}

# Widgets
@app.websocket("/ws/weather")
async def websocket_weather(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            temperature = await weather.get_user_temperature()
            description = await weather.get_user_weather_description()
            precipitation = await weather.get_user_precipitation()
            user_location = location.get_city()

            data = {
                "temperature": temperature,
                "description": description,
                "location": user_location,
                "precipitation": precipitation
            }
            disconnected = []
            for client in connected_clients:
                try:
                    await client.send_json(data)
                except WebSocketDisconnect:
                    disconnected.append(client)
            for client in disconnected:
                connected_clients.remove(client)

            await asyncio.sleep(300) # 5 Minutes
    except WebSocketDisconnect:
        connected_clients.remove(websocket)