from django.shortcuts import render
from amadeus import Client, ResponseError
from django.conf import settings
from django.http import JsonResponse
import json

def home(request):
    amadeus = Client(
        client_id=settings.AMADEUS_CLIENT_ID,
        client_secret=settings.AMADEUS_CLIENT_SECRET
    )

    if request.GET:
        try:
            # Print search parameters for debugging
            print("Search Parameters:", request.GET)
            
            cityCode = request.GET.get('cityCode', '').upper()
            checkInDate = request.GET.get('checkIn')
            checkOutDate = request.GET.get('checkOut')
            adults = int(request.GET.get('adults', 1))

            # Try searching for hotels using amadeus.reference_data first
            try:
                hotels_list = amadeus.reference_data.locations.hotels.by_city.get(
                    cityCode=cityCode
                )
                hotel_ids = [hotel['hotelId'] for hotel in hotels_list.data][:20]
                
                # Then get offers for specific hotels
                hotel_offers = amadeus.shopping.hotel_offers_search.get(
                    hotelIds=hotel_ids,
                    checkInDate=checkInDate,
                    checkOutDate=checkOutDate,
                    adults=adults,
                    roomQuantity=1,
                    currency='USD'
                )
                
                print("API Response:", hotel_offers.data)
                
                return render(request, 'hotels/home.html', {
                    'hotels': hotel_offers.data,
                    'search_params': request.GET
                })
            
            except ResponseError as api_error:
                print("Detailed API Error:", api_error.response.body)  # Print full error response
                raise api_error

        except ResponseError as error:
            return render(request, 'hotels/home.html', {
                'error': f"Search Error: {str(error)}",
                'search_params': request.GET
            })
        except Exception as e:
            print("General Error:", str(e))
            return render(request, 'hotels/home.html', {
                'error': f"An error occurred: {str(e)}",
                'search_params': request.GET
            })
    
    return render(request, 'hotels/home.html')

def search_cities(request):
    amadeus = Client(
        client_id=settings.AMADEUS_CLIENT_ID,
        client_secret=settings.AMADEUS_CLIENT_SECRET
    )
    
    keyword = request.GET.get('keyword', '')
    try:
        response = amadeus.reference_data.locations.get(
            keyword=keyword,
            subType='CITY',
            
        )
        print("City Search Response:", response.data) 
        return JsonResponse(response.data, safe=False)
    except ResponseError as error:
        print("City Search Error:", str(error))
        return JsonResponse({'error': str(error)}, status=400)