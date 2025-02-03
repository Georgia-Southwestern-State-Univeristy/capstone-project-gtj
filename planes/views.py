from django.shortcuts import render
from django.http import JsonResponse
from amadeus import Client, ResponseError
from django.conf import settings
from rest_framework.views import APIView  # Add this import
from rest_framework.response import Response  # Add this import
from datetime import datetime

def home(request):
    amadeus = Client(
        client_id=settings.AMADEUS_CLIENT_ID,
        client_secret=settings.AMADEUS_CLIENT_SECRET
    )

    if request.GET:
        try:
            origin = request.GET.get('origin', '').upper()
            destination = request.GET.get('destination', '').upper()
            ldate = request.GET.get('departure_date'),
            rdate = request.GET.get('return_date'),
            passengers = request.GET.get('adults', 1)

            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=ldate,
                returnDate=rdate,
                adults=int(passengers),
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


class FlightDataView(APIView):
    def get(self, request):
        amadeus = Client(
            client_id=settings.AMADEUS_CLIENT_ID,
            client_secret=settings.AMADEUS_CLIENT_SECRET
        )

        try:
            origin = request.GET.get('origin', '').upper()
            destination = request.GET.get('destination', '').upper()
            ldate = request.GET.get('departure_date'),
            rdate = request.GET.get('return_date'),
            passengers = request.GET.get('adults', 1),
            

            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=ldate,
                returnDate=rdate,
                adults=int(passengers),
                currencyCode='USD'
            )
            
            return Response(response.data)
            
        except ResponseError as error:
            return Response({'error': str(error)}, status=400)