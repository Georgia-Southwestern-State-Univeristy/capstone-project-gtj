from django.shortcuts import render

def safety_search(request):
    return render(request, 'safety/safety.html')

def safety_results(request):
    if request.GET:
        city = request.GET.get('city', '')
        date = request.GET.get('date', '')
        # In a real application, you would process this data and fetch safety information
        # For now, we'll just pass the parameters to the template
        context = {
            'city': city,
            'date': date,
        }
        return render(request, 'safety/safety_results.html', context)
    return render(request, 'safety/safety_results.html')