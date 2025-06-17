import os
import math
import requests
from typing import Optional, Tuple

from backend.logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################


def get_coordinates(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "GAIA/1.0"
    }
    response = requests.get(url, params=params, headers=headers, timeout=5)
    response.raise_for_status()
    data = response.json()
    
    if data:
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat, lon
    else:
        return None, None

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_km = R * c

    return distance_km


def distance_to_place(city1, city2) -> Optional[float]:
    lat1, lon1 = get_coordinates(city1)
    lat2, lon2 = get_coordinates(city2)
    
    if None in (lat1, lon1, lat2, lon2):
        return None
    
    return haversine_distance(lat1, lon1, lat2, lon2)

def get_user_location() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("city"), data.get("region"), data.get("country")
    except requests.RequestException as e:
        logger.error(f"Failed to get user location from IP: {e}")
        return None, None, None

if __name__ == "__main__":
    city, region, country = get_user_location()
    user_location = f'{city}, {region}, {country}'
    print(distance_to_place(user_location, "Toronto Ontario Canada"))
