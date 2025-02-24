from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests
from hotels.cache_utils import api_cache
import logging

logger = logging.getLogger(__name__)

def home(request):
    """Home view for transport app"""
    return render(request, 'transport/home.html')

@api_cache.cached_api_call('transit_search')
def search_transport(request):
    """Search transit options for a city"""
    context = {}
    
    if request.GET.get('city'):
        try:
            city = request.GET.get('city').strip()
            
            # First get the city coordinates using Geocoding API
            location_data = get_city_coordinates(city)
            
            if location_data and location_data.get('status') == 'OK':
                location = location_data['results'][0]['geometry']['location']
                formatted_address = location_data['results'][0]['formatted_address']
                
                # Then get all transit stations
                transit_data = get_transit_stations(location)
                
                if transit_data and transit_data.get('status') == 'OK':
                    # Organize stations by type
                    stations = categorize_stations(transit_data.get('results', []))
                    
                    context.update({
                        'city': formatted_address,
                        'location': location,
                        'stations': stations,
                        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
                    })
                else:
                    context['error'] = 'No transit stations found'
            else:
                context['error'] = 'City not found'
                
        except Exception as e:
            logger.error(f"Transit search error: {str(e)}")
            context['error'] = 'An error occurred while searching for transit options'
    
    return render(request, 'transport/search_results.html', context)

def get_city_coordinates(city):
    """Get coordinates for a city using Google Geocoding API"""
    try:
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': city,
            'key': settings.GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(geocode_url, params=params)
        return response.json()
    except Exception as e:
        logger.error(f"Geocoding error: {str(e)}")
        return None

def get_transit_stations(location):
    """Get transit stations near a location"""
    try:
        places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'location': f"{location['lat']},{location['lng']}",
            'radius': '10000',  # 10km radius for better coverage
            'type': ['subway_station', 'train_station', 'bus_station', 'transit_station'],
            'key': settings.GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(places_url, params=params)
        return response.json()
    except Exception as e:
        logger.error(f"Places API error: {str(e)}")
        return None

def categorize_stations(stations):
    """Categorize stations by type"""
    categorized = {
        'subway': [],
        'train': [],
        'bus': [],
        'other': []
    }
    
    for station in stations:
        station_types = station.get('types', [])
        
        # Determine station type
        station_type = 'other'
        if 'subway_station' in station_types:
            station_type = 'subway'
        elif 'train_station' in station_types:
            station_type = 'train'
        elif 'bus_station' in station_types or 'transit_station' in station_types:
            station_type = 'bus'
        
        # Add station to appropriate category with details
        categorized[station_type].append({
            'name': station['name'],
            'address': station.get('vicinity', ''),
            'location': station['geometry']['location'],
            'rating': station.get('rating', 'N/A'),
            'place_id': station.get('place_id', ''),
            'types': station_types,
            'icon': station.get('icon', ''),
            'photos': station.get('photos', [])
        })
    
    return categorized

@api_cache.cached_api_call('station_details')
def get_station_details(request):
    """Get detailed information about a specific station"""
    try:
        station_id = request.GET.get('station_id')
        if not station_id:
            return JsonResponse({'error': 'Station ID is required'}, status=400)
            
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'place_id': station_id,
            'fields': 'name,formatted_address,opening_hours,website,formatted_phone_number,photos,rating,reviews',
            'key': settings.GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(details_url, params=params)
        return JsonResponse(response.json())
        
    except Exception as e:
        logger.error(f"Station details error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@api_cache.cached_api_call('transit_routes')
def get_routes(request):
    """Get transit routes between two points"""
    try:
        origin = request.GET.get('origin')
        destination = request.GET.get('destination')
        
        if not all([origin, destination]):
            return JsonResponse({'error': 'Origin and destination are required'}, status=400)
            
        directions_url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            'origin': origin,
            'destination': destination,
            'mode': 'transit',
            'alternatives': 'true',
            'key': settings.GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(directions_url, params=params)
        routes_data = response.json()
        
        if routes_data.get('status') == 'OK':
            return JsonResponse(routes_data)
        else:
            return JsonResponse({
                'error': 'No routes found',
                'details': routes_data.get('status')
            }, status=404)
            
    except Exception as e:
        logger.error(f"Routes error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)