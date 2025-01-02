import random
import math
import requests
from largest_cities import largest_cities
from config import AZURE_MAPS_API_KEY
import logging

def generate_coordinates():
    cities = largest_cities() 
    city = random.choice(cities)  

    max_radius_km = 50  
    max_radius_deg = max_radius_km * 0.009  

    angle = random.uniform(0, 2 * math.pi)
    radius = random.uniform(0, max_radius_deg)

    lat_offset = radius * math.cos(angle)
    lon_offset = radius * math.sin(angle)
    lat = city["latitude"] + lat_offset
    lon = city["longitude"] + lon_offset

    return lat, lon

def get_address_from_coordinates(lat, lon, api_key):
    url = "https://atlas.microsoft.com/search/address/reverse/json"
    params = {
        'api-version': '1.0',
        'subscription-key': api_key,
        'query': f"{lat},{lon}",
        'language': 'sv-SE',
        'countrySet': 'SE'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        addresses = data.get('addresses', [])

        if addresses:
            address_info = addresses[0].get('address', {})
            street = address_info.get('streetName', 'No Street')
            house_number = address_info.get('streetNumber', '')
            postcode = address_info.get('postalCode', 'No Postcode')
            city = address_info.get('municipalitySubdivision', 'No City')
            municipality = address_info.get('municipality', 'No Municipality')

            full_street = f"{street} {house_number}".strip()
            return full_street, postcode, city, municipality
        else:
            return "No Street", "No Postcode", "No City", "No Municipality"
    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
        return "No Street", "No Postcode", "No City", "No Municipality"