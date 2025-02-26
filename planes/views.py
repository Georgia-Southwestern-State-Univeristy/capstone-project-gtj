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
def api_debug(request):
    """
    API debugging view for planes app to test Amadeus flight API calls
    and handle edge cases
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
        'test_cases': None
    }
    
    # Default search parameters
    today = datetime.now()
    future_date = today + timedelta(days=30)  # A month in the future
    future_date_str = future_date.strftime('%Y-%m-%d')
    return_date = future_date + timedelta(days=7)
    return_date_str = return_date.strftime('%Y-%m-%d')
    
    context['default_dates'] = {
        'departure': future_date_str,
        'return': return_date_str
    }
    
    # Common test cases
    test_cases = [
        {'name': 'Invalid Origin', 'origin': 'XYZ', 'destination': 'LON', 'departure_date': future_date_str},
        {'name': 'Invalid Destination', 'origin': 'NYC', 'destination': 'XYZ', 'departure_date': future_date_str},
        {'name': 'Past Date', 'origin': 'NYC', 'destination': 'LON', 'departure_date': '2020-01-01'},
        {'name': 'Same Day Return', 'origin': 'NYC', 'destination': 'LON', 'departure_date': future_date_str, 'return_date': future_date_str},
        {'name': 'Return Before Departure', 'origin': 'NYC', 'destination': 'LON', 'departure_date': future_date_str, 'return_date': today.strftime('%Y-%m-%d')},
        {'name': 'Zero Passengers', 'origin': 'NYC', 'destination': 'LON', 'departure_date': future_date_str, 'adults': 0}
    ]
    
    context['test_cases'] = test_cases
    
    if request.method == 'POST':
        try:
            # Get form data
            api_call_type = request.POST.get('api_call_type')
            
            # Basic search parameters
            origin = request.POST.get('origin', '').strip().upper()
            destination = request.POST.get('destination', '').strip().upper()
            departure_date = request.POST.get('departure_date')
            return_date = request.POST.get('return_date', '')
            adults = int(request.POST.get('adults', 1))
            
            # Validation
            errors = []
            
            if not origin or len(origin) != 3:
                errors.append("Origin must be a valid 3-letter IATA code")
                
            if not destination or len(destination) != 3:
                errors.append("Destination must be a valid 3-letter IATA code")
                
            if not departure_date:
                errors.append("Departure date is required")
                
            if adults < 1:
                errors.append("At least one adult passenger is required")
                
            # Check for past dates
            try:
                departure_date_obj = datetime.strptime(departure_date, '%Y-%m-%d')
                if departure_date_obj < today:
                    errors.append("Warning: Departure date is in the past")
                    
                if return_date:
                    return_date_obj = datetime.strptime(return_date, '%Y-%m-%d')
                    if return_date_obj < departure_date_obj:
                        errors.append("Warning: Return date is before departure date")
            except ValueError:
                errors.append("Invalid date format")
                
            if errors:
                context['error'] = ", ".join(errors)
                return render(request, 'planes/api_debug.html', context)
            
            context['request_params'] = {
                'api_call_type': api_call_type,
                'origin': origin,
                'destination': destination,
                'departure_date': departure_date,
                'return_date': return_date,
                'adults': adults
            }
            
            # Execute API call based on type
            if api_call_type == 'airport_search':
                # Test airport search endpoint
                keyword = origin if origin else "NYC"  # Use origin as search term or default
                response = amadeus.reference_data.locations.get(
                    keyword=keyword,
                    subType=["AIRPORT"],
                    page={'limit': 10}
                )
                context['results'] = response.data
                context['api_response'] = json.dumps(response.data, indent=2)
                
            elif api_call_type == 'flight_search':
                # Test flight search endpoint with specified parameters
                search_params = {
                    'originLocationCode': origin,
                    'destinationLocationCode': destination,
                    'departureDate': departure_date,
                    'adults': adults,
                    'currencyCode': 'USD',
                    'max': 5  # Limit results for display
                }
                
                if return_date:
                    search_params['returnDate'] = return_date
                
                response = amadeus.shopping.flight_offers_search.get(**search_params)
                
                context['results'] = response.data
                context['api_response'] = json.dumps(response.data[:3], indent=2)  # Limit JSON for display
                
            elif api_call_type == 'flight_prices':
                # Test flight price analysis
                # First get some flight offers
                search_params = {
                    'originLocationCode': origin,
                    'destinationLocationCode': destination,
                    'departureDate': departure_date,
                    'adults': adults,
                    'currencyCode': 'USD',
                    'max': 2  # Just get a couple offers for price check
                }
                
                if return_date:
                    search_params['returnDate'] = return_date
                
                flight_offers = amadeus.shopping.flight_offers_search.get(**search_params)
                
                if flight_offers.data:
                    # Get price analysis for the first offer
                    flight_price = amadeus.shopping.flight_offers.pricing.post(
                        flight_offers.data[:1]  # Just the first offer
                    )
                    context['results'] = flight_price.data
                    context['api_response'] = json.dumps(flight_price.data, indent=2)
                else:
                    context['error'] = "No flight offers found to analyze prices"
                
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
    
    return render(request, 'planes/api_debug.html', context)