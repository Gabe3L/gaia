import os
import asyncio

import python_weather

import backend.app.apis.online.location as location
from backend.logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

def fetch_weather(city: str) -> str:
    with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = client.get(city)

        weather_report = (f"Iron Man, today the weather in {weather.location} is {weather.description.lower()}, with a temperature of {weather.temperature} degrees Celcius.")

        return weather_report

async def get_user_temperature() -> str:
    city = location.get_city()

    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(city)

        return weather.temperature

async def get_user_weather_description() -> str:
    city = location.get_city()

    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(city)
        return weather.description
    
async def get_user_precipitation() -> str:
    city = location.get_city()

    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(city)
        return weather.precipitation

################################################################

if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    print(asyncio.run(get_user_weather_description()))