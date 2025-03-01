from django.shortcuts import render
from django.http import JsonResponse
from amadeus import Client, ResponseError
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

def get_amadeus_client():
    """Helper function to get Amadeus client instance"""
    return Client(
        client_id=settings.AMADEUS_CLIENT_ID,
        client_secret=settings.AMADEUS_CLIENT_SECRET
    )

def get_booking_links(flight):
    """Generate booking links for multiple platforms"""
    booking_links = {}
    
    # Only process if we have the necessary data
    if 'itineraries' in flight and flight['itineraries'] and flight['itineraries'][0]['segments']:
        # Extract basic flight information
        outbound = flight['itineraries'][0]['segments'][0]
        origin = outbound['departure']['iataCode']
        destination = outbound['arrival']['iataCode']
        
        # Format departure date (YYYY-MM-DD)
        departure_date = outbound['departure']['at']
        if 'T' in departure_date:
            departure_date = departure_date.split('T')[0]
            
        # Get airline information if available
        airline_code = outbound.get('carrierCode', '')
        flight_number = outbound.get('number', '')
        
        # Check for return flight
        return_date = None
        if len(flight['itineraries']) > 1 and flight['itineraries'][1]['segments']:
            return_flight = flight['itineraries'][1]['segments'][0]
            return_date = return_flight['departure']['at']
            if 'T' in return_date:
                return_date = return_date.split('T')[0]
        
        # Generate Google Flights link
        google_url = "https://www.google.com/travel/flights?hl=en&gl=US"
        google_url += f"&q=flights%20from%20{origin}%20to%20{destination}%20on%20{departure_date}"
        if return_date:
            google_url += f"%20returning%20on%20{return_date}"
        if airline_code:
            google_url += f"%20on%20{airline_code}"
        booking_links['google'] = google_url
        
        # Generate Kayak link
        kayak_url = f"https://www.kayak.com/flights/{origin}-{destination}/{departure_date}"
        if return_date:
            kayak_url += f"/{return_date}"
        if airline_code:
            kayak_url += f"/{airline_code}"
        kayak_url += f"?sort=bestflight_a"
        booking_links['kayak'] = kayak_url
        
        # Generate Expedia link
        expedia_url = "https://www.expedia.com/Flights-Search?trip="
        if return_date:
            expedia_url += f"roundtrip&leg1={origin},{destination},{departure_date}&leg2={destination},{origin},{return_date}"
        else:
            expedia_url += f"oneway&leg1={origin},{destination},{departure_date}"
        expedia_url += "&passengers=adults:1,children:0,seniors:0,infantinlap:Y&mode=search"
        booking_links['expedia'] = expedia_url
    
    return booking_links

def home(request):
    """Main view for the flight search page"""
    if request.GET:
        try:
            # Clean and validate input data
            origin = request.GET.get('origin', '').strip().upper()
            destination = request.GET.get('destination', '').strip().upper()
            departure_date = request.GET.get('departure_date')
            return_date = request.GET.get('return_date')
            adults = int(request.GET.get('adults', 1))
            direct_only = request.GET.get('direct_only', 'on')  # Add a checkbox in the form

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
                'adults': adults,
                'currencyCode': 'USD',
                'max': 50  # Increase max results to ensure we get enough after filtering
            }

            # Add return date if provided
            if return_date:
                search_params['returnDate'] = return_date

            # Get Amadeus client and make API call
            amadeus = get_amadeus_client()
            
            # Make API call with detailed error logging
            try:
                logger.info(f"Flight search with params: {search_params}")
                response = amadeus.shopping.flight_offers_search.get(**search_params)
                logger.info(f"Found {len(response.data)} flight offers")
                
                # Filter for direct flights if requested
                flight_data = response.data
                if direct_only == 'on':
                    flight_data = [
                        flight for flight in response.data 
                        if all(len(itinerary['segments']) == 1 for itinerary in flight['itineraries'])
                    ]
                    logger.info(f"Filtered to {len(flight_data)} direct flights")
                
                # Process the flight data to add booking links
                for flight in flight_data:
                    # Generate booking links for multiple platforms
                    booking_links = get_booking_links(flight)
                    flight['booking_links'] = booking_links
                
                return render(request, 'planes/home.html', {
                    'flights': flight_data,
                    'search_params': search_params,
                    'direct_only': direct_only == 'on'
                })
            
            except ResponseError as api_error:
                logger.error(f"Amadeus API error: {str(api_error)}")
                try:
                    error_details = json.loads(api_error.response.body)
                    error_message = error_details.get('errors', [{}])[0].get('detail', str(api_error))
                except:
                    error_message = str(api_error)
                
                return render(request, 'planes/home.html', {
                    'error': f"Flight search error: {error_message}",
                    'search_params': search_params
                })

        except Exception as e:
            logger.exception(f"Unexpected error in flight search: {str(e)}")
            return render(request, 'planes/home.html', {
                'error': f"An unexpected error occurred: {str(e)}"
            })
    
    # If no search parameters, just render the empty form
    return render(request, 'planes/home.html')


def search_airports(request):
    """
    API endpoint to search for airports by keyword
    Used for autocomplete functionality
    """
    amadeus = get_amadeus_client()
    keyword = request.GET.get('keyword', '').strip()
    if len(keyword) < 2:
        return JsonResponse([], safe=False)
        
    try:
        logger.info(f"Airport search for keyword: {keyword}")
        
        response = amadeus.reference_data.locations.get(
            keyword=keyword,
            subType=["AIRPORT"],
            page={'limit': 10}
        )
        
        logger.debug(f"Found {len(response.data)} airports")
        return JsonResponse(response.data, safe=False)
    
    except ResponseError as error:
        logger.error(f"Airport search error: {str(error)}")
        return JsonResponse({'error': str(error)}, status=400)
    except Exception as e:
        logger.exception(f"Unexpected error in airport search: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

class FlightDataView(APIView):
    """REST API endpoint for flight data (optional, for AJAX calls)"""
    def get(self, request):
        amadeus = get_amadeus_client()
        try:
            # Clean and validate input data
            origin = request.GET.get('origin', '').strip().upper()
            destination = request.GET.get('destination', '').strip().upper()
            departure_date = request.GET.get('departure_date')
            return_date = request.GET.get('return_date')
            adults = int(request.GET.get('adults', 1))

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
                'adults': adults,
                'currencyCode': 'USD'
            }

            # Add return date if provided
            if return_date:
                search_params['returnDate'] = return_date

            # Make API call
            response = amadeus.shopping.flight_offers_search.get(**search_params)
            return Response(response.data)
           
        except ResponseError as error:
            logger.error(f"API Error in FlightDataView: {str(error)}")
            return Response({
                'error': str(error),
                'search_params': search_params if 'search_params' in locals() else None
            }, status=400)
        except Exception as error:
            logger.exception(f"Unexpected error in FlightDataView: {str(error)}")
            return Response({
                'error': f"An error occurred: {str(error)}"
            }, status=400)

def api_debug(request):
    """
    API debugging view for planes app to test Amadeus flight API calls
    and handle edge cases
    """
    amadeus = get_amadeus_client()
    
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