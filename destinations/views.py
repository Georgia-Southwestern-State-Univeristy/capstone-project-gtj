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