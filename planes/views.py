from django.shortcuts import render
from django.http import JsonResponse
from amadeus import Client, ResponseError
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

   
def search_airports(request):
    amadeus = Client(
        client_id=settings.AMADEUS_CLIENT_ID,
        client_secret=settings.AMADEUS_CLIENT_SECRET
    )
   
    keyword = request.GET.get('keyword', '').strip()
    if len(keyword) < 2:
        return JsonResponse([], safe=False)
        
    try:
        response = amadeus.reference_data.locations.get(
            keyword=keyword,
            subType=["AIRPORT"],
            page={'limit': 10}
        )
        return JsonResponse(response.data, safe=False)
    except ResponseError as error:
        return JsonResponse({'error': str(error)}, status=400)

class FlightDataView(APIView):
    def get(self, request):
        amadeus = Client(
            client_id=settings.AMADEUS_CLIENT_ID,
            client_secret=settings.AMADEUS_CLIENT_SECRET
        )
        try:
            # Clean and validate input data
            origin = request.GET.get('origin', '').strip().upper()
            destination = request.GET.get('destination', '').strip().upper()
            departure_date = request.GET.get('departure_date')
            return_date = request.GET.get('return_date')
            passengers = request.GET.get('adults', 1)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

            
            if not all([origin, destination, departure_date]):
                return Response({
                    'error': 'Origin, destination, and departure date are required.'
                }, status=400)

            # Basic IATA code validation
            if len(origin) != 3 or len(destination) != 3:
                return Response({
                    'error': 'Invalid airport code. Please use 3-letter IATA codes.'
                }, status=400)

            # Create search parameters
            search_params = {
                'originLocationCode': origin,
                'destinationLocationCode': destination,
                'departureDate': departure_date,
                'adults': int(passengers),
                'currencyCode': 'USD'
            }

            # Add return date if provided
            if return_date:
                search_params['returnDate'] = return_date
from common.cache_utils import api_cache
import logging

logger = logging.getLogger(__name__)

def get_amadeus_client():
    return Client(
        client_id=settings.AMADEUS_CLIENT_ID,
        client_secret=settings.AMADEUS_CLIENT_SECRET
    )

@api_cache.cached_api_call('airports', timeout=86400)  # Cache airports for 24 hours
def search_airports(request):
    try:
        amadeus = get_amadeus_client()
        keyword = request.GET.get('keyword', '').strip()
        
        if len(keyword) < 2:
            return JsonResponse([], safe=False)
            
        response = amadeus.reference_data.locations.get(
            keyword=keyword,
            subType=["AIRPORT"],
            page={'limit': 10}
        )
        return JsonResponse(response.data, safe=False)
        
    except Exception as e:
        logger.error(f"Airport search error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

@api_cache.cached_api_call('flights', timeout=1800)  # Cache flights for 30 minutes
def search_flights(request):
    try:
        amadeus = get_amadeus_client()
        origin = request.GET.get('origin', '').strip().upper()
        destination = request.GET.get('destination', '').strip().upper()
        departure_date = request.GET.get('departure_date')
        return_date = request.GET.get('return_date')
        adults = request.GET.get('adults', 1)

        search_params = {
            'originLocationCode': origin,
            'destinationLocationCode': destination,
            'departureDate': departure_date,
            'adults': int(adults),
            'currencyCode': 'USD'
        }

        if return_date:
            search_params['returnDate'] = return_date

        response = amadeus.shopping.flight_offers_search.get(**search_params)
        return JsonResponse(response.data, safe=False)
        
    except Exception as e:
        logger.error(f"Flight search error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

def home(request):
    return render(request, 'planes/home.html')