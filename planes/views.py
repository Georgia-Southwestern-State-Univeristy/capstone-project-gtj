from django.shortcuts import render
from django.http import JsonResponse
from amadeus import Client, ResponseError
from django.conf import settings

def home(request):
    amadeus = Client(
        client_id=settings.AMADEUS_CLIENT_ID,
        client_secret=settings.AMADEUS_CLIENT_SECRET
    )

    if request.GET:
        try:
            origin = request.GET.get('origin', '').upper()
            destination = request.GET.get('destination', '').upper()
            departure_date = request.GET.get('departure_date')
            return_date = request.GET.get('return_date')
            adults = int(request.GET.get('adults', 2))

            # Make API call
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=departure_date,
                returnDate=return_date,
                adults=adults,
                currencyCode='USD'
            )
            
            return render(request, 'planes/home.html', {'flights': response.data})
            
        except ResponseError as error:
            return render(request, 'planes/home.html', {'error': error})
    
    return render(request, 'planes/home.html')

def search_airports(request):
    amadeus = Client(
        client_id=settings.AMADEUS_CLIENT_ID,
        client_secret=settings.AMADEUS_CLIENT_SECRET
    )
    
    keyword = request.GET.get('keyword', '')
    try:
        response = amadeus.reference_data.locations.get(
            keyword=keyword,
            subType=["AIRPORT"],
            page={'limit': 10}
        )
        return JsonResponse(response.data, safe=False)
    except ResponseError as error:
        return JsonResponse({'error': str(error)}, status=400)