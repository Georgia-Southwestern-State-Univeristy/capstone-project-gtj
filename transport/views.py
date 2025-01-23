from django.shortcuts import render
def transport(request):
    return render(request, 'transport/home.html')

# Create your views here.
from django.http import HttpResponse


def transport(request):
    return HttpResponse("This is the transport index page.")