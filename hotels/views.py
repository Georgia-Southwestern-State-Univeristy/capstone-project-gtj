from django.shortcuts import render
from amadeus import Client, ResponseError
from django.conf import settings
from django.http import JsonResponse
from .cache_utils import api_cache
import logging

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