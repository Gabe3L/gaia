import os
import requests
import geocoder
import webbrowser

from geopy.geocoders import Nominatim
from geopy.distance import great_circle

from logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

def distance_to_place(place) -> tuple[str, dict, float]:
    webbrowser.open("http://www.google.com/maps/place/" + place + "")
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(place, addressdetails=True)
    target_latlng = location.latitude, location.longitude
    location = location.raw['address']
    target_loc = {'city': location.get('city', ''),
                   'country': location.get('country', '')}

    current_loc = geocoder.ip('me')
    current_latlng = current_loc.latlng

    distance = str(great_circle(current_latlng, target_latlng))
    distance = str(distance.split(' ',1)[0])
    distance = round(float(distance), 2)

    return current_loc, target_loc, distance

def my_location() -> tuple[str, str]:
    ip_add = requests.get('https://api.ipify.org').text
    url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
    geo_requests = requests.get(url)
    geo_data = geo_requests.json()
    city = geo_data['city']
    country = geo_data['country']

    return city, country