from django.shortcuts import render
from django.db import models
from .models import CountrySafety
from .utils import get_country_safety_info
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def safety_search(request):
    """
    View for the safety search page where users can search for country safety information.
    """
    return render(request, 'safety/safety.html')

def safety_results(request):
    country_query = request.GET.get('country', '')
    
    if country_query:
        try:
            # Try to find the country by name or code
            country = CountrySafety.objects.filter(
                models.Q(name__icontains=country_query) | 
                models.Q(code__iexact=country_query)
            ).first()
            
            if country:
                # Check if country has safety info
                if not country.safety_summary:
                    # No safety info in database, try to get from Claude
                    
                    # Check cache first
                    cache_key = f"safety_info_{country.code}"
                    safety_info = cache.get(cache_key)
                    
                    if not safety_info:
                        # Get from Claude API
                        safety_info = get_country_safety_info(country.name)
                        
                        # Cache the result for a week
                        if safety_info:
                            cache.set(cache_key, safety_info, 60*60*24*7)
                    
                    # Update country with generated info (don't save to database)
                    if safety_info:
                        country.safety_summary = safety_info.get('safety_summary', '')
                        country.women_safety_info = safety_info.get('women_safety_info', '')
                        country.night_safety_info = safety_info.get('night_safety_info', '')
                        country.solo_traveler_info = safety_info.get('solo_traveler_info', '')
                        country.crime_info = safety_info.get('crime_info', '')
                        country.transportation_safety_info = safety_info.get('transportation_safety_info', '')
                        country.emergency_numbers = safety_info.get('emergency_numbers', '')
                
                context = {'country': country}
            else:
                # Country not found in database, try direct Claude API
                safety_info = get_country_safety_info(country_query)
                
                if safety_info:
                    # Create a temporary country object (not saved to database)
                    country = CountrySafety(
                        name=country_query,
                        code="",
                        safety_summary=safety_info.get('safety_summary', ''),
                        women_safety_info=safety_info.get('women_safety_info', ''),
                        night_safety_info=safety_info.get('night_safety_info', ''),
                        solo_traveler_info=safety_info.get('solo_traveler_info', ''),
                        crime_info=safety_info.get('crime_info', ''),
                        transportation_safety_info=safety_info.get('transportation_safety_info', ''),
                        emergency_numbers=safety_info.get('emergency_numbers', ''),
                        overall_safety_score=50,
                        women_safety_score=50,
                        night_safety_score=50,
                        crime_score=50
                    )
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
@login_required
def save_country_info(request, country_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Staff only")
        
    country = get_object_or_404(CountrySafety, id=country_id)
    
    # Get latest info from Claude
    safety_info = get_country_safety_info(country.name)
    
    if safety_info:
        country.safety_summary = safety_info.get('safety_summary', '')
        country.women_safety_info = safety_info.get('women_safety_info', '')
        country.night_safety_info = safety_info.get('night_safety_info', '')
        country.solo_traveler_info = safety_info.get('solo_traveler_info', '')
        country.crime_info = safety_info.get('crime_info', '')
        country.transportation_safety_info = safety_info.get('transportation_safety_info', '')
        country.emergency_numbers = safety_info.get('emergency_numbers', '')
        country.save()
        
        messages.success(request, f"Safety information for {country.name} updated")
    else:
        messages.error(request, f"Failed to get safety information for {country.name}")
    
    return redirect('admin:safety_countrysafety_change', object_id=country.id)