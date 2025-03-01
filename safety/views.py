from django.db import models
from django.shortcuts import render
from .models import CountrySafety

def safety_search(request):
    """
    View for the safety search page where users can search for country safety information.
    """
    return render(request, 'safety/safety.html')

def safety_results(request):
    country_query = request.GET.get('country', '')
    
    if country_query:
        # Try to find the country by name or code
        try:
            country = CountrySafety.objects.filter(
                models.Q(name__icontains=country_query) | 
                models.Q(code__iexact=country_query)
            ).first()
            
            if country:
                context = {'country': country}
            else:
                context = {
                    'error': f"Sorry, we don't have safety information for {country_query} yet.",
                    'country_query': country_query
                }
        except Exception as e:
            context = {
                'error': f"An error occurred: {str(e)}",
                'country_query': country_query
            }
    else:
        context = {}
    
    return render(request, 'safety/safety_results.html', context)