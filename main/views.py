from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse

def index(request):
	return HttpResponse("This is the main index page.")
