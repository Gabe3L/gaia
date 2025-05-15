import os
import asyncio
from queue import Queue
from typing import List
from pathlib import Path
from threading import Event

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect

from backend.logs.logging_setup import setup_logger
from backend.app.processor import Gaia, ThreadManager
from backend.app.apis.online import *
from backend.app.apis.offline import *

#####################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

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
        logger.info("Weather websocket disconnected")
        connected_clients.remove(websocket)
    except Exception as e:
        logger.error(e)

@app.websocket("/ws/spotify")
async def websocket_spotify(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            artist = await spotify.get_this_artist()
            title = await spotify.get_this_title()
            timestamp = await spotify.get_this_timestamp()
            total_time = await spotify.get_this_total_time()
            album_cover = await spotify.get_this_album_cover()
            next_artist = await spotify.get_next_artist()
            next_title = await spotify.get_next_title()

            data = {
                "artist": artist,
                "title": title,
                "timestamp": timestamp,
                "total_time": total_time,
                "album_cover": album_cover,
                "next_artist": next_artist,
                "next_title": next_title
            }
            disconnected = []
            for client in connected_clients:
                try:
                    await client.send_json(data)
                except WebSocketDisconnect:
                    disconnected.append(client)
            for client in disconnected:
                connected_clients.remove(client)

            await asyncio.sleep(2)
    except WebSocketDisconnect:
        logger.info("Spotify websocket disconnected")
        connected_clients.remove(websocket)
    except Exception as e:
        logger.error(e)
        
@app.websocket("/ws/calendar")
async def websocket_calendar(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            date = await google_calendar.get_date()
            first_day = await google_calendar.get_first_day()
            event_titles = await google_calendar.get_event_titles()

            data = {
                "date": date,
                "first_day": first_day,
                "event_titles": event_titles
            }
            disconnected = []
            for client in connected_clients:
                try:
                    await client.send_json(data)
                except WebSocketDisconnect:
                    disconnected.append(client)
            for client in disconnected:
                connected_clients.remove(client)

            await asyncio.sleep(2)
    except WebSocketDisconnect:
        logger.info("Spotify websocket disconnected")
        connected_clients.remove(websocket)
    except Exception as e:
        logger.error(e)
        
@app.websocket("/ws/clock")
async def websocket_clock(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            minute = await date_time.get_minute()
            hour = await date_time.get_hour()
            day = await date_time.get_day()
            month = await date_time.get_month()
            year = await date_time.get_year()

            data = {
                "minute": minute,
                "hour": hour,
                "day": day,
                "month": month,
                "year": year
            }
            disconnected = []
            for client in connected_clients:
                try:
                    await client.send_json(data)
                except WebSocketDisconnect:
                    disconnected.append(client)
            for client in disconnected:
                connected_clients.remove(client)

            await asyncio.sleep(2)
    except WebSocketDisconnect:
        logger.info("Spotify websocket disconnected")
        connected_clients.remove(websocket)
    except Exception as e:
        logger.error(e)
        
@app.websocket("/ws/webcam")
async def websocket_webcam(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    # try:
    #     while True:
    #         artist = await spotify.get_this_artist()
    #         title = await spotify.get_this_title()
    #         timestamp = await spotify.get_this_timestamp()
    #         total_time = await spotify.get_this_total_time()
    #         album_cover = await spotify.get_this_album_cover()
    #         next_artist = await spotify.get_next_artist()
    #         next_title = await spotify.get_next_title()

    #         data = {
    #             "artist": artist,
    #             "title": title,
    #             "timestamp": timestamp,
    #             "total_time": total_time,
    #             "album_cover": album_cover,
    #             "next_artist": next_artist,
    #             "next_title": next_title
    #         }
    #         disconnected = []
    #         for client in connected_clients:
    #             try:
    #                 await client.send_json(data)
    #             except WebSocketDisconnect:
    #                 disconnected.append(client)
    #         for client in disconnected:
    #             connected_clients.remove(client)

    #         await asyncio.sleep(2)
    # except WebSocketDisconnect:
    #     logger.info("Spotify websocket disconnected")
    #     connected_clients.remove(websocket)
    # except Exception as e:
    #     logger.error(e)
        
@app.websocket("/ws/system")
async def websocket_system(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    # try:
    #     while True:
    #         artist = await spotify.get_this_artist()
    #         title = await spotify.get_this_title()
    #         timestamp = await spotify.get_this_timestamp()
    #         total_time = await spotify.get_this_total_time()
    #         album_cover = await spotify.get_this_album_cover()
    #         next_artist = await spotify.get_next_artist()
    #         next_title = await spotify.get_next_title()

    #         data = {
    #             "artist": artist,
    #             "title": title,
    #             "timestamp": timestamp,
    #             "total_time": total_time,
    #             "album_cover": album_cover,
    #             "next_artist": next_artist,
    #             "next_title": next_title
    #         }
    #         disconnected = []
    #         for client in connected_clients:
    #             try:
    #                 await client.send_json(data)
    #             except WebSocketDisconnect:
    #                 disconnected.append(client)
    #         for client in disconnected:
    #             connected_clients.remove(client)

    #         await asyncio.sleep(2)
    # except WebSocketDisconnect:
    #     logger.info("Spotify websocket disconnected")
    #     connected_clients.remove(websocket)
    # except Exception as e:
    #     logger.error(e)
        
@app.websocket("/ws/email")
async def websocket_email(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    # try:
    #     while True:
    #         artist = await spotify.get_this_artist()
    #         title = await spotify.get_this_title()
    #         timestamp = await spotify.get_this_timestamp()
    #         total_time = await spotify.get_this_total_time()
    #         album_cover = await spotify.get_this_album_cover()
    #         next_artist = await spotify.get_next_artist()
    #         next_title = await spotify.get_next_title()

    #         data = {
    #             "artist": artist,
    #             "title": title,
    #             "timestamp": timestamp,
    #             "total_time": total_time,
    #             "album_cover": album_cover,
    #             "next_artist": next_artist,
    #             "next_title": next_title
    #         }
    #         disconnected = []
    #         for client in connected_clients:
    #             try:
    #                 await client.send_json(data)
    #             except WebSocketDisconnect:
    #                 disconnected.append(client)
    #         for client in disconnected:
    #             connected_clients.remove(client)

    #         await asyncio.sleep(2)
    # except WebSocketDisconnect:
    #     logger.info("Spotify websocket disconnected")
    #     connected_clients.remove(websocket)
    # except Exception as e:
    #     logger.error(e)