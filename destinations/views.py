from django.shortcuts import render
import requests

def country_info(request):
    # Get query from either the homepage search or the destination page search
    query = request.GET.get('query') or request.GET.get('country', '')
    
    if not query:
        return render(request, 'destinations/country.html')
    
    try:
        # First try to search for city
        geocode_response = requests.get(
            f'https://nominatim.openstreetmap.org/search',
            params={
                'q': query,
                'format': 'json',
                'addressdetails': 1,
                'limit': 1
            },
            headers={'User-Agent': 'GTJGoApp/1.0'}
        )
        
        city_data = None
        country_data = None
        travel_tips = []

        if geocode_response.status_code == 200 and geocode_response.json():
            city_data = geocode_response.json()[0]
            country_code = city_data.get('address', {}).get('country_code', '').upper()
            
            # Get city details using a travel API (example using RestCountries for country info)
            if country_code:
                country_response = requests.get(f'https://restcountries.com/v3.1/alpha/{country_code}')
                if country_response.status_code == 200:
                    country_data = country_response.json()[0]
                    
                    # Add travel tips based on the country/city
                    travel_tips = generate_travel_tips(city_data, country_data)

        # If no city found or want to search country directly
        if not city_data:
            country_response = requests.get(f'https://restcountries.com/v3.1/name/{query}')
            if country_response.status_code == 200:
                country_data = country_response.json()[0]
                travel_tips = generate_travel_tips(None, country_data)
        
        if city_data or country_data:
            context = {
                'city': city_data,
                'country': country_data,
                'travel_tips': travel_tips,
                'query': query
            }
            return render(request, 'destinations/country.html', context)
        
        return render(request, 'destinations/country.html', {
            'error': f'Could not find information for {query}',
            'query': query
        })
        
    except Exception as e:
        return render(request, 'destinations/country.html', {
            'error': f'An error occurred: {str(e)}',
            'query': query
        })

def generate_travel_tips(city_data, country_data):
    """Generate travel tips based on city and country data"""
    tips = []
    
    if country_data:
        # Currency tips
        currencies = country_data.get('currencies', {})
        for currency in currencies.values():
            tips.append({
                'category': 'Currency',
                'tip': f"The local currency is {currency.get('name')} ({currency.get('symbol')}). "
                      "It's recommended to have some local currency for small purchases."
            })
            
        # Language tips
        languages = country_data.get('languages', {}).values()
        if languages:
            lang_list = ', '.join(languages)
            tips.append({
                'category': 'Language',
                'tip': f"The main language(s) spoken are {lang_list}. "
                      "Consider learning basic greetings and phrases."
            })

    if city_data:
        # Location tips
        address = city_data.get('address', {})
        if address.get('city') and address.get('country'):
            tips.append({
                'category': 'Location',
                'tip': f"Located in {address.get('country')}, {address.get('city')} "
                      "can be explored through public transportation or guided tours."
            })

        # Add seasonal tips based on hemisphere
        lat = float(city_data.get('lat', 0))
        if lat > 0:
            tips.append({
                'category': 'Weather',
                'tip': "Located in the Northern Hemisphere. Summer is June-August, "
                      "Winter is December-February."
            })
        else:
            tips.append({
                'category': 'Weather',
                'tip': "Located in the Southern Hemisphere. Summer is December-February, "
                      "Winter is June-August."
            })

    # Add general travel tips
    tips.append({
        'category': 'Safety',
        'tip': "Keep important documents safe and make digital copies. "
              "Be aware of your surroundings and keep emergency numbers handy."
    })

    return tips