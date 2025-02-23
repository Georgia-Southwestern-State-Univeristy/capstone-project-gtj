from django.shortcuts import render
from amadeus import Client, ResponseError
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests

def get_city_coordinates(city_name):
    """Get latitude and longitude for a city using Google Geocoding API"""
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&key={settings.GOOGLE_MAPS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        return None, None
    except Exception as e:
        print(f"Geocoding error: {str(e)}")
        return None, None

def city_info(request):
    amadeus = Client(
        client_id=settings.AMADEUS_CLIENT_ID,
        client_secret=settings.AMADEUS_CLIENT_SECRET
    )

    if request.GET.get('city'):
        try:
            city = request.GET.get('city').upper()
            city_name = request.GET.get('city_name', city)  # For geocoding
            
            # Get city coordinates
            lat, lng = get_city_coordinates(city_name)
            if lat is None or lng is None:
                return render(request, 'destinations/city_info.html', {
                    'error': 'Could not find coordinates for this city'
                })

            # Points of Interest
            try:
                pois = amadeus.reference_data.locations.points_of_interest.get(
                    latitude=lat,
                    longitude=lng,
                    radius=20
                )
                points_of_interest = pois.data
            except ResponseError as e:
                print(f"POI Error: {str(e)}")
                points_of_interest = []

            # Tours and Activities
            try:
                activities = amadeus.shopping.activities.get(
                    latitude=lat,
                    longitude=lng,
                    radius=20
                )
                tours_activities = activities.data
            except ResponseError as e:
                print(f"Activities Error: {str(e)}")
                tours_activities = []

            # Hotels
            try:
                hotels = amadeus.reference_data.locations.hotels.by_city.get(
                    cityCode=city
                )
                hotel_list = hotels.data
            except ResponseError as e:
                print(f"Hotels Error: {str(e)}")
                hotel_list = []

            context = {
                'city': city,
                'city_name': city_name,
                'latitude': lat,
                'longitude': lng,
                'points_of_interest': points_of_interest,
                'tours_activities': tours_activities,
                'hotels': hotel_list,
                'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
            }

            return render(request, 'destinations/city_info.html', context)

        except Exception as e:
            return render(request, 'destinations/city_info.html', {
                'error': f"An error occurred: {str(e)}"
            })

    return render(request, 'destinations/city_info.html')
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests
from common.cache_utils import api_cache
import logging

logger = logging.getLogger(__name__)

@api_cache.cached_api_call('city_info', timeout=86400)  # Cache for 24 hours
def get_city_info(request):
    try:
        city = request.GET.get('city', '').strip()
        
        # Get city coordinates
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': city,
            'key': settings.GOOGLE_MAPS_API_KEY
        }
        
        geocode_response = requests.get(geocode_url, params=params)
        location_data = geocode_response.json()
        
        if location_data['status'] == 'OK':
            location = location_data['results'][0]['geometry']['location']
            
            # Get points of interest
            places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            poi_params = {
                'location': f"{location['lat']},{location['lng']}",
                'radius': '5000',
                'type': 'tourist_attraction',
                'key': settings.GOOGLE_MAPS_API_KEY
            }
            
            places_response = requests.get(places_url, params=poi_params)
            poi_data = places_response.json()
            
            return JsonResponse({
                'city': location_data['results'][0]['formatted_address'],
                'location': location,
                'points_of_interest': poi_data['results']
            })
            
    except Exception as e:
        logger.error(f"City info error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

@api_cache.cached_api_call('weather', timeout=1800)  # Cache for 30 minutes
def get_weather(request):
    try:
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        
        # Get weather data
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': settings.OPENWEATHER_API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(weather_url, params=params)
        return JsonResponse(response.json())
        
    except Exception as e:
        logger.error(f"Weather error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

def city_info(request):
    return render(request, 'destinations/city_info.html')