from queue import Queue
from threading import Event
from fastapi import FastAPI, BackgroundTasks
from backend.app.processor import Gaia, ThreadManager

app = FastAPI()

gaia = Gaia()
thread_manager = ThreadManager(gaia)

stop_event = Event()
speech_queue = Queue()
command_queue = Queue()

@app.post("/start-processing/")
async def start_processing(background_tasks: BackgroundTasks):
    background_tasks.add_task(thread_manager.start_all_threads, stop_event, speech_queue, command_queue)

    return {"message": "Processing started!"}

@app.post("/stop-processing/")
async def stop_processing():
    stop_event.set()
    thread_manager.close_all_threads()
    return {"message": "Processing stopped!"}

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}