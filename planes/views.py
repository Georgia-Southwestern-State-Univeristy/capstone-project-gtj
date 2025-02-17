from django.shortcuts import render
from django.http import JsonResponse
from amadeus import Client, ResponseError
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

def home(request):
    amadeus = Client(
        client_id=settings.AMADEUS_CLIENT_ID,
        client_secret=settings.AMADEUS_CLIENT_SECRET
    )
    
    if request.GET:
        try:
            # Clean and validate input data
            origin = request.GET.get('origin', '').strip().upper()
            destination = request.GET.get('destination', '').strip().upper()
            departure_date = request.GET.get('departure_date')
            return_date = request.GET.get('return_date')
            passengers = request.GET.get('adults', 1)

            # Validate required fields
            if not all([origin, destination, departure_date]):
                return render(request, 'planes/home.html', {
                    'error': 'Origin, destination, and departure date are required.'
                })

            # Basic IATA code validation
            if len(origin) != 3 or len(destination) != 3:
                return render(request, 'planes/home.html', {
                    'error': 'Invalid airport code. Please use 3-letter IATA codes.'
                })

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

            # Make API call
            response = amadeus.shopping.flight_offers_search.get(**search_params)
            
            return render(request, 'planes/home.html', {
                'flights': response.data,
                'search_params': search_params  # Useful for debugging
            })
           
        except ResponseError as error:
            return render(request, 'planes/home.html', {
                'error': f"API Error: {str(error)}",
                'search_params': search_params if 'search_params' in locals() else None
            })
        except ValueError as error:
            return render(request, 'planes/home.html', {
                'error': f"Invalid input: {str(error)}"
            })
   
    return render(request, 'planes/home.html')
   
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

            # Validate required fields
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

            # Make API call
            response = amadeus.shopping.flight_offers_search.get(**search_params)
           
            return Response(response.data)
           
        except ResponseError as error:
            return Response({
                'error': str(error),
                'search_params': search_params if 'search_params' in locals() else None
            }, status=400)
        except ValueError as error:
            return Response({
                'error': f"Invalid input: {str(error)}"
            }, status=400)
