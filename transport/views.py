# transport/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests
from hotels.cache_utils import api_cache  # Using the same cache utility
import logging

logger = logging.getLogger(__name__)

def home(request):
    """Home view for transport app"""
    return render(request, 'transport/home.html')

@api_cache.cached_api_call('transport_options')
def get_transport_options(request):
    """Get available transport options for a city"""
    try:
        city = request.GET.get('city', '').strip()
        
        # Get city coordinates
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': city,
            'key': settings.GOOGLE_MAPS_API_KEY
        }
        
        geocode_response = requests.get(geocode_url, params=params)
        location_data = geocode_response.json()
        
        if location_data['status'] == 'OK':
            location = location_data['results'][0]['geometry']['location']
            
            # Get transit stations
            places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            transit_params = {
                'location': f"{location['lat']},{location['lng']}",
                'radius': '5000',
                'type': 'transit_station',
                'key': settings.GOOGLE_MAPS_API_KEY
            }
            
            places_response = requests.get(places_url, params=transit_params)
            transit_data = places_response.json()
            
            return JsonResponse({
                'city': location_data['results'][0]['formatted_address'],
                'location': location,
                'stations': transit_data.get('results', [])
            })
            
        return JsonResponse({'error': 'City not found'}, status=404)
        
    except Exception as e:
        logger.error(f"Transport API error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@api_cache.cached_api_call('transport_routes')
def get_routes(request):
    """Get transit routes between two points"""
    try:
        origin = request.GET.get('origin')
        destination = request.GET.get('destination')
        
        # Validate inputs
        if not all([origin, destination]):
            return JsonResponse({'error': 'Origin and destination are required'}, status=400)
            
        # Get transit directions
        directions_url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            'origin': origin,
            'destination': destination,
            'mode': 'transit',
            'alternatives': 'true',
            'key': settings.GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(directions_url, params=params)
        return JsonResponse(response.json())
        
    except Exception as e:
        logger.error(f"Routes API error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)