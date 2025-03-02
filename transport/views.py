from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def home(request):
    """Home view for transport app"""
    return render(request, 'transport/home.html')

def search_transport(request):
    """Search transit options for a city or address"""
    context = {}
    
    if request.GET.get('location'):
        try:
            location = request.GET.get('location').strip()
            
            # First get the location coordinates using Geocoding API
            location_data = get_location_coordinates(location)
            
            if location_data and location_data.get('status') == 'OK':
                place = location_data['results'][0]
                coordinates = place['geometry']['location']
                formatted_address = place['formatted_address']
                
                # Get nearby transit stations
                transit_stations = get_nearby_transit(coordinates)
                
                # Get additional transit info if specific stations are selected
                selected_station = request.GET.get('station_id')
                transit_routes = None
                
                if selected_station:
                    # Get upcoming departures and route details for selected station
                    transit_routes = get_station_routes(selected_station, coordinates)
                
                context.update({
                    'location': formatted_address,
                    'coordinates': coordinates,
                    'stations': transit_stations,
                    'selected_station': selected_station,
                    'transit_routes': transit_routes,
                    'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
                })
            else:
                context['error'] = 'Location not found'
                
        except Exception as e:
            logger.error(f"Transit search error: {str(e)}")
            context['error'] = f'An error occurred: {str(e)}'
    
    return render(request, 'transport/search_results.html', context)

def get_location_coordinates(location):
    """Get coordinates for a location using Google Geocoding API"""
    try:
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': location,
            'key': settings.GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(geocode_url, params=params)
        return response.json()
    except Exception as e:
        logger.error(f"Geocoding error: {str(e)}")
        return None

def get_nearby_transit(coordinates):
    """Get transit stations near coordinates"""
    try:
        places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'location': f"{coordinates['lat']},{coordinates['lng']}",
            'radius': '1500',  # 1.5km radius
            'type': 'transit_station',
            'key': settings.GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(places_url, params=params)
        results = response.json()
        
        # Categorize stations and get more details
        stations = []
        if results.get('status') == 'OK':
            for station in results.get('results', []):
                # Determine station type based on types field
                station_type = get_station_type(station.get('types', []))
                
                # Get station details including place_id for later use
                stations.append({
                    'id': station.get('place_id'),
                    'name': station.get('name'),
                    'type': station_type,
                    'location': station.get('geometry', {}).get('location'),
                    'vicinity': station.get('vicinity'),
                    'rating': station.get('rating', 'N/A'),
                    'icon': station.get('icon')
                })
        
        # Group stations by type
        grouped_stations = {
            'subway': [],
            'train': [],
            'bus': [],
            'other': []
        }
        
        for station in stations:
            station_type = station['type']
            if station_type in grouped_stations:
                grouped_stations[station_type].append(station)
            else:
                grouped_stations['other'].append(station)
                
        return grouped_stations
        
    except Exception as e:
        logger.error(f"Places API error: {str(e)}")
        return None

def get_station_type(type_list):
    """Determine station type from Google Places type list"""
    if 'subway_station' in type_list:
        return 'subway'
    elif 'train_station' in type_list:
        return 'train'
    elif 'bus_station' in type_list:
        return 'bus'
    else:
        return 'other'

def get_station_routes(station_id, origin_coordinates):
    """Get routes from a specific station including departure times"""
    try:
        # First get detailed place information
        place_url = "https://maps.googleapis.com/maps/api/place/details/json"
        place_params = {
            'place_id': station_id,
            'fields': 'name,geometry,formatted_address',
            'key': settings.GOOGLE_MAPS_API_KEY
        }
        
        place_response = requests.get(place_url, params=place_params)
        place_data = place_response.json()
        
        if place_data.get('status') != 'OK':
            return None
            
        station_info = place_data.get('result', {})
        station_location = station_info.get('geometry', {}).get('location', {})
        
        # Then get transit directions from this station
        directions_url = "https://maps.googleapis.com/maps/api/directions/json"
        
        # We'll get routes starting from this station to a few nearby points
        # to capture different transit lines
        routes = []
        
        # Get routes in different directions (north, south, east, west)
        for bearing in [0, 90, 180, 270]:
            # Calculate destination point roughly 5km away in this direction
            dest_coords = calculate_destination(
                station_location.get('lat'),
                station_location.get('lng'),
                bearing,
                5  # 5km distance
            )
            
            directions_params = {
                'origin': f"{station_location.get('lat')},{station_location.get('lng')}",
                'destination': f"{dest_coords[0]},{dest_coords[1]}",
                'mode': 'transit',
                'departure_time': 'now',
                'alternatives': 'true',
                'key': settings.GOOGLE_MAPS_API_KEY
            }
            
            directions_response = requests.get(directions_url, params=directions_params)
            directions_data = directions_response.json()
            
            if directions_data.get('status') == 'OK':
                # Process and extract relevant route information
                for route in directions_data.get('routes', []):
                    for leg in route.get('legs', []):
                        for step in leg.get('steps', []):
                            if step.get('travel_mode') == 'TRANSIT':
                                transit_details = step.get('transit_details', {})
                                
                                if transit_details:
                                    # Extract departure times, line information, etc.
                                    line = transit_details.get('line', {})
                                    departure_time = transit_details.get('departure_time', {})
                                    arrival_time = transit_details.get('arrival_time', {})
                                    
                                    route_info = {
                                        'line_name': line.get('name', 'Unknown'),
                                        'line_short_name': line.get('short_name', ''),
                                        'line_color': line.get('color', '#CCCCCC'),
                                        'line_text_color': line.get('text_color', '#000000'),
                                        'line_vehicle': line.get('vehicle', {}).get('type', 'BUS'),
                                        'departure_time': departure_time.get('text', ''),
                                        'departure_timestamp': departure_time.get('value', 0),
                                        'arrival_time': arrival_time.get('text', ''),
                                        'num_stops': transit_details.get('num_stops', 0),
                                        'departure_stop': transit_details.get('departure_stop', {}).get('name', ''),
                                        'arrival_stop': transit_details.get('arrival_stop', {}).get('name', '')
                                    }
                                    
                                    # Only add unique routes
                                    if not any(r.get('line_name') == route_info['line_name'] and 
                                              r.get('line_short_name') == route_info['line_short_name'] for r in routes):
                                        routes.append(route_info)
        
        # Sort routes by departure time
        routes.sort(key=lambda x: x.get('departure_timestamp', 0))
        
        return {
            'station_name': station_info.get('name', ''),
            'station_address': station_info.get('formatted_address', ''),
            'routes': routes
        }
        
    except Exception as e:
        logger.error(f"Routes error: {str(e)}")
        return None

def calculate_destination(lat, lng, bearing, distance):
    """
    Calculate destination point given starting lat/long, bearing in degrees,
    and distance in kilometers using a simplified flat-earth approximation
    """
    import math
    
    # Constants for Earth
    R = 6371  # Earth's radius in km
    
    # Convert to radians
    lat_rad = math.radians(lat)
    lng_rad = math.radians(lng)
    bearing_rad = math.radians(bearing)
    
    # Calculate destination point
    lat2_rad = math.asin(math.sin(lat_rad) * math.cos(distance/R) + 
                          math.cos(lat_rad) * math.sin(distance/R) * math.cos(bearing_rad))
    
    lng2_rad = lng_rad + math.atan2(math.sin(bearing_rad) * math.sin(distance/R) * math.cos(lat_rad),
                                    math.cos(distance/R) - math.sin(lat_rad) * math.sin(lat2_rad))
    
    # Convert back to degrees
    lat2 = math.degrees(lat2_rad)
    lng2 = math.degrees(lng2_rad)
    
    return (lat2, lng2)

def get_transit_stations(request):
    """AJAX endpoint to get transit stations near a location"""
    try:
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        
        if not lat or not lng:
            return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)
            
        # Get nearby stations
        stations = get_nearby_transit({'lat': float(lat), 'lng': float(lng)})
        return JsonResponse({'stations': stations})
        
    except Exception as e:
        logger.error(f"Transit stations error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

def get_routes(request):
    """AJAX endpoint to get routes for a station"""
    try:
        station_id = request.GET.get('station_id')
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        
        if not station_id or not lat or not lng:
            return JsonResponse({'error': 'Station ID, latitude, and longitude are required'}, status=400)
            
        # Get station routes
        routes = get_station_routes(station_id, {'lat': float(lat), 'lng': float(lng)})
        return JsonResponse({'routes': routes})
        
    except Exception as e:
        logger.error(f"Routes error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)