from django.shortcuts import render
from amadeus import Client, ResponseError
from django.conf import settings
from django.http import JsonResponse

def home(request):
    amadeus = Client(
        client_id=settings.AMADEUS_CLIENT_ID,
        client_secret=settings.AMADEUS_CLIENT_SECRET
    )

    if request.GET:
        try:
            # Get parameters from form
            start_location = request.GET.get('pickupLocation', '').upper()
            end_location = request.GET.get('dropoffLocation', '').upper()
            pickup_date = request.GET.get('pickupDate')
            passengers = int(request.GET.get('passengers', 1))

            print("Search Parameters:", {
                'start_location': start_location,
                'end_location': end_location,
                'pickup_date': pickup_date,
                'passengers': passengers
            })

            transfers = amadeus.shopping.transfers.get(
                startLocationCode=start_location,
                endLocationCode=end_location,
                startDateTime=f"{pickup_date}T10:00:00",
                passengerQuantity=passengers,
                currency='USD'
            )
            
            print("Transfer Response:", transfers.data)
            
            return render(request, 'transport/home.html', {
                'transfers': transfers.data,
                'search_params': request.GET
            })
            
        except ResponseError as error:
            print("API Error:", error.response.body)
            return render(request, 'transport/home.html', {
                'error': str(error),
                'search_params': request.GET
            })
    
    return render(request, 'transport/home.html')

def search_locations(request):
    amadeus = Client(
        client_id=settings.AMADEUS_CLIENT_ID,
        client_secret=settings.AMADEUS_CLIENT_SECRET
    )
    
    keyword = request.GET.get('keyword', '')
    try:
        response = amadeus.reference_data.locations.get(
            keyword=keyword,
            subType='CITY'
        )
        return JsonResponse(response.data, safe=False)
    except ResponseError as error:
        return JsonResponse({'error': str(error)}, status=400)