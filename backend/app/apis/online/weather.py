import os

import python_weather

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

if __name__ == '__main__':
    logger.debug(fetch_weather('London, Ontario'))