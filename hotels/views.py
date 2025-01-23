
from django.shortcuts import render
def hotels(request):
	return render(request, 'hotels/home.html')
from django.shortcuts import HttpResponse

def hotels(request):
	return HttpResponse("This is a temporaryu placeholder. Hotel Bookings should show up here")
