from django.shortcuts import render
from amadeus import Client, ResponseError
from django.conf import settings
from django.http import JsonResponse
from .cache_utils import api_cache
import logging
import json

logger = logging.getLogger(__name__)

def get_amadeus_client():
    return Client(
        client_id=settings.AMADEUS_CLIENT_ID,
        client_secret=settings.AMADEUS_CLIENT_SECRET
    )

@api_cache.cached_api_call('cities')
def search_cities(request):
    """Search cities with caching"""
    try:
        amadeus = get_amadeus_client()
        keyword = request.GET.get('keyword', '').strip()
        
        if len(keyword) < 2:
            return JsonResponse([], safe=False)
            
        response = amadeus.reference_data.locations.get(
            keyword=keyword,
            subType='CITY'
        )
        return JsonResponse(response.data, safe=False)
        
    except ResponseError as e:
        logger.error(f"Amadeus API error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

def home(request):
    context = {'search_params': request.GET}
    
    if request.GET:
        try:
            amadeus = get_amadeus_client()
            city_code = request.GET.get('cityCode', '').upper()
            check_in = request.GET.get('checkIn')
            check_out = request.GET.get('checkOut')
            adults = int(request.GET.get('adults', 1))

            # Get hotels list
            hotels_response = amadeus.reference_data.locations.hotels.by_city.get(
                cityCode=city_code
            )
            hotel_ids = [hotel['hotelId'] for hotel in hotels_response.data][:20]
            
            # Get hotel offers
            hotel_offers = amadeus.shopping.hotel_offers_search.get(
                hotelIds=hotel_ids,
                checkInDate=check_in,
                checkOutDate=check_out,
                adults=adults,
                roomQuantity=1,
                currency='USD'
            )
            
            context['hotels'] = hotel_offers.data
            
        except ResponseError as e:
            logger.error(f"Amadeus API error: {str(e)}")
            context['error'] = f"Search Error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            context['error'] = "An unexpected error occurred"
    
    return render(request, 'hotels/home.html', context)
def api_debug(request):
    """
    API debugging view for hotels app to test Amadeus API calls
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
        'api_response': None
    }
    
    if request.method == 'POST':
        try:
            # Get form data
            api_call_type = request.POST.get('api_call_type')
            cityCode = request.POST.get('cityCode', '').strip().upper()
            
            # Basic validation
            if not cityCode or len(cityCode) != 3:
                context['error'] = "Please provide a valid 3-letter IATA city code"
                return render(request, 'hotels/api_debug.html', context)
            
            context['request_params'] = {
                'api_call_type': api_call_type,
                'cityCode': cityCode
            }
            
            # Execute API call based on type
            if api_call_type == 'city_search':
                # Test city search endpoint
                response = amadeus.reference_data.locations.get(
                    keyword=cityCode,
                    subType='CITY'
                )
                context['results'] = response.data
                context['api_response'] = json.dumps(response.data, indent=2)
                
            elif api_call_type == 'hotels_by_city':
                # Test hotels by city endpoint
                response = amadeus.reference_data.locations.hotels.by_city.get(
                    cityCode=cityCode
                )
                hotels = response.data
                context['results'] = hotels[:10] if hotels else []  # Limit to 10 for display
                context['api_response'] = json.dumps(hotels[:10] if hotels else [], indent=2)
                
            elif api_call_type == 'hotel_offers':
                # Test hotel offers endpoint with minimal parameters
                # First get hotel IDs
                hotels_list = amadeus.reference_data.locations.hotels.by_city.get(
                    cityCode=cityCode
                )
                hotel_ids = [hotel['hotelId'] for hotel in hotels_list.data][:5]  # Limit to 5
                
                # Then get offers
                checkIn = request.POST.get('checkIn')
                checkOut = request.POST.get('checkOut')
                
                if not checkIn or not checkOut:
                    context['error'] = "Check-in and check-out dates are required for hotel offers"
                    return render(request, 'hotels/api_debug.html', context)
                
                response = amadeus.shopping.hotel_offers_search.get(
                    hotelIds=hotel_ids,
                    checkInDate=checkIn,
                    checkOutDate=checkOut,
                    adults=1,
                    roomQuantity=1,
                    currency='USD'
                )
                
                context['results'] = response.data
                context['api_response'] = json.dumps(response.data, indent=2)
                
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
    
    return render(request, 'hotels/api_debug.html', context)