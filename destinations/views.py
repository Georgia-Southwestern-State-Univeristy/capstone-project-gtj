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
def api_debug(request):
    """
    API debugging view for destinations app to test Amadeus and Google Maps APIs
    """
    amadeus = Client(
        client_id=settings.AMADEUS_CLIENT_ID,
        client_secret=settings.AMADEUS_CLIENT_SECRET
    )
    
    context = {
        'results': None,
        'request_params': None,
        'error': None,
        'api_response': None,
        'city_data': None,
        'map_data': None
    }
    
    if request.method == 'POST':
        try:
            # Get form data
            api_call_type = request.POST.get('api_call_type')
            city_code = request.POST.get('city_code', '').strip().upper()
            city_name = request.POST.get('city_name', '').strip()
            
            # If city name is not provided, use city code as name
            if not city_name:
                city_name = city_code
                
            # Basic validation
            if api_call_type in ['poi', 'activities'] and (not city_code or len(city_code) != 3):
                context['error'] = "Please provide a valid 3-letter IATA city code"
                return render(request, 'destinations/api_debug.html', context)
                
            context['request_params'] = {
                'api_call_type': api_call_type,
                'city_code': city_code,
                'city_name': city_name
            }
            
            # Get coordinates for the city regardless of API call type
            # This is needed for most API calls and helps detect geocoding issues early
            lat, lng = None, None
            
            if api_call_type != 'geocode':  # Don't get coordinates if testing geocoding
                lat, lng = get_city_coordinates(city_name)
                if not lat or not lng:
                    context['error'] = f"Could not get coordinates for {city_name}. Please check the city name or try another location."
                    return render(request, 'destinations/api_debug.html', context)
                    
                context['map_data'] = {
                    'lat': lat,
                    'lng': lng
                }
            
            # Execute API call based on type
            if api_call_type == 'geocode':
                # Test Google Maps Geocoding API
                context['api_response'] = test_geocode_api(city_name)
                context['results'] = json.loads(context['api_response'])
                
                # Extract coordinates if successful
                if context['results'].get('status') == 'OK' and context['results'].get('results'):
                    location = context['results']['results'][0]['geometry']['location']
                    context['map_data'] = {
                        'lat': location['lat'],
                        'lng': location['lng']
                    }
                
            elif api_call_type == 'poi':
                # Test points of interest API
                if not lat or not lng:
                    context['error'] = "Coordinates required for Points of Interest"
                    return render(request, 'destinations/api_debug.html', context)
                    
                try:
                    pois = amadeus.reference_data.locations.points_of_interest.get(
                        latitude=lat,
                        longitude=lng,
                        radius=20
                    )
                    context['results'] = pois.data
                    context['api_response'] = json.dumps(pois.data, indent=2)
                except ResponseError as e:
                    raise e
                
            elif api_call_type == 'activities':
                # Test tours and activities API
                if not lat or not lng:
                    context['error'] = "Coordinates required for Activities"
                    return render(request, 'destinations/api_debug.html', context)
                    
                try:
                    activities = amadeus.shopping.activities.get(
                        latitude=lat,
                        longitude=lng,
                        radius=20
                    )
                    context['results'] = activities.data
                    context['api_response'] = json.dumps(activities.data, indent=2)
                except ResponseError as e:
                    raise e
                
            elif api_call_type == 'city_hotels':
                # Test hotels by city API
                try:
                    hotels = amadeus.reference_data.locations.hotels.by_city.get(
                        cityCode=city_code
                    )
                    context['results'] = hotels.data[:20]  # Limit to first 20 for display
                    context['api_response'] = json.dumps(hotels.data[:20], indent=2)
                except ResponseError as e:
                    raise e
                
        except ResponseError as error:
            logger.error(f"Amadeus API Error: {str(error)}")
            error_details = None
            
            # Extract detailed error information if available
            try:
                error_details = json.loads(error.response.body)
            except:
                error_details = {'message': str(error)}
                
            context['error'] = f"API Error: {str(error)}"
            context['api_response'] = json.dumps(error_details, indent=2)
            
        except Exception as e:
            logger.exception(f"General error in API debug: {str(e)}")
            context['error'] = f"An error occurred: {str(e)}"
    
    return render(request, 'destinations/api_debug.html', context)

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
        logger.error(f"Geocoding error: {str(e)}")
        return None, None

def test_geocode_api(city_name):
    """Test the Google Maps Geocoding API directly"""
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&key={settings.GOOGLE_MAPS_API_KEY}"
        response = requests.get(url)
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        logger.error(f"Geocoding test error: {str(e)}")
        return json.dumps({"error": str(e)})