import requests

from core.config import tmap_api_key


class TmapService:
    def __init__(self):
        self.geocoding_url = "https://apis.openapi.sk.com/tmap/geo/geocoding"

    def get_lat_and_lon_from_geocoding(self, city_do: str, gu_gun: str, dong: str, bunji: str):
        params = {
            'version': '1',
            'city_do': city_do,
            'gu_gun': gu_gun,
            'dong': dong,
            'bunji': bunji,
            'addressFlag': 'F00',
            'coordType': 'WGS84GEO'
        }

        headers = {
            'Accept': 'application/json',
            'appKey': tmap_api_key
        }

        response = requests.get(self.geocoding_url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
        else:
            raise Exception("Tmap Geocoding Error")

        if data.get('coordinateInfo').get('lat') == "":
            lat = data.get('coordinateInfo').get('newLat')
        else:
            lat = data.get('coordinateInfo').get('lat')

        if data.get('coordinateInfo').get('lon') == "":
            lon = data.get('coordinateInfo').get('newLon')
        else:
            lon = data.get('coordinateInfo').get('lon')

        result = {
            'lat': lat,
            'lon': lon
        }

        return result