from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Favorite
import json

@login_required
def add_favorite(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            favorite_type = data.get('type')
            item_data = data.get('item_data')

            # Create favorite if it doesn't exist
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                type=favorite_type,
                item_data=item_data
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Added to favorites' if created else 'Already in favorites'
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def remove_favorite(request, favorite_id):
    try:
        favorite = Favorite.objects.get(id=favorite_id, user=request.user)
        favorite.delete()
        return JsonResponse({'status': 'success', 'message': 'Removed from favorites'})
    except Favorite.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Favorite not found'}, status=404)

@login_required
def view_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).order_by('-created_at')
    
    # Organize favorites by type
    context = {
        'flights': favorites.filter(type='FLIGHT'),
        'hotels': favorites.filter(type='HOTEL'),
        'countries': favorites.filter(type='COUNTRY')
    }
    
    return render(request, 'favorites/favorites.html', context)