from django.shortcuts import render, redirect
from .models import Airport, Ride
from .forms import RideForm

def home(request):
    return render(request, 'transport/home.html')

def ride_request(request):
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.user = request.user
            ride.save()
            return redirect('ride_confirmation')
    else:
        form = RideForm()
    return render(request, 'ride_request.html', {'form': form})

def ride_confirmation(request):
    return render(request, 'ride_confirmation.html')
def ride_list(request):
    if request.method == 'POST':
        airport = request.POST['airport']
        date = request.POST['date']
        hotel = request.POST['hotel']
        
        # Here, you can perform any necessary operations with the form data,
        # such as filtering available rides based on the airport, date, and hotel.
        # For now, we'll just pass the form data to the template.
        
        context = {
            'airport': airport,
            'date': date,
            'hotel': hotel,
            'rides': [
                {'driver': 'John', 'car': 'Toyota Camry', 'price': 50},
                {'driver': 'Jane', 'car': 'Honda Civic', 'price': 45},
                {'driver': 'Mike', 'car': 'Ford Mustang', 'price': 60},
            ],
        }
        return render(request, 'transport/ride_list.html', context)
    
    return render(request, 'transport/home.html')