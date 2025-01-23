from django.shortcuts import render
def planes(request):
    return render(request, 'planes/home.html')

# Create your views here
# .
from django.http import HttpResponse


def planes(request):
    return HttpResponse("This is the planes index page.")