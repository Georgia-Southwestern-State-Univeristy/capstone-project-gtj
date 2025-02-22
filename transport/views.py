from django.shortcuts import render
from django.db.models import Prefetch
from .models import City, TransitPass, TransitLine, TransitStation

def home(request):
    return render(request, 'transport/home.html')

def search_transit(request):
    city_query = request.GET.get('city', '').strip()
    
    if city_query:
        try:
            # Get city and all related transit information
            city = City.objects.prefetch_related(
                'transit_passes',
                'transit_lines',
                Prefetch(
                    'transit_lines__stations',
                    queryset=TransitStation.objects.filter(accessibility=True)
                )
            ).get(name__iexact=city_query)
            
            # Organize transit lines by type
            transit_types = {}
            for line in city.transit_lines.all():
                type_name = line.get_line_type_display()
                if type_name not in transit_types:
                    transit_types[type_name] = {
                        'lines': [],
                        'icon': get_transit_icon(line.line_type)  # Helper function to get icon
                    }
                transit_types[type_name]['lines'].append(line)
            
            # Organize passes by type
            passes = {}
            for pass_obj in city.transit_passes.all():
                type_name = pass_obj.get_pass_type_display()
                if type_name not in passes:
                    passes[type_name] = []
                passes[type_name].append(pass_obj)
            
            context = {
                'city': city,
                'transit_types': transit_types,
                'passes': passes,
                'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
            }
            
            return render(request, 'transport/search_results.html', context)
            
        except City.DoesNotExist:
            return render(request, 'transport/home.html', {
                'error': f"Sorry, we don't have transit information for {city_query} yet."
            })
    
    return render(request, 'transport/home.html')

def get_transit_icon(transit_type):
    """Helper function to return appropriate icon class for each transit type"""
    icons = {
        'METRO': 'subway',
        'BUS': 'bus',
        'TRAM': 'train',
        'TRAIN': 'train',
        'FERRY': 'ship',
        'BIKE': 'bicycle',
    }
    return icons.get(transit_type, 'question-circle')