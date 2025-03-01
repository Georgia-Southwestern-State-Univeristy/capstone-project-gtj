from django.shortcuts import render
import requests
from django.conf import settings
from django.http import JsonResponse
from decimal import Decimal
import json

def currency_converter(request):
    """
    Render the currency converter page and handle conversion requests
    """
    # List of common currencies for dropdown
    currencies = [
        {"code": "USD", "name": "US Dollar"},
        {"code": "EUR", "name": "Euro"},
        {"code": "GBP", "name": "British Pound"},
        {"code": "JPY", "name": "Japanese Yen"},
        {"code": "AUD", "name": "Australian Dollar"},
        {"code": "CAD", "name": "Canadian Dollar"},
        {"code": "CHF", "name": "Swiss Franc"},
        {"code": "CNY", "name": "Chinese Yuan"},
        {"code": "INR", "name": "Indian Rupee"},
        {"code": "MXN", "name": "Mexican Peso"},
        {"code": "SGD", "name": "Singapore Dollar"},
        {"code": "THB", "name": "Thai Baht"},
        {"code": "NZD", "name": "New Zealand Dollar"},
        {"code": "KRW", "name": "South Korean Won"},
        {"code": "AED", "name": "UAE Dirham"},
    ]
    
    result = None
    amount = 1
    from_currency = "USD"
    to_currency = "EUR"
    error = None
    
    if request.method == "GET" and 'amount' in request.GET:
        try:
            amount = Decimal(request.GET.get('amount', 1))
            from_currency = request.GET.get('from_currency', 'USD')
            to_currency = request.GET.get('to_currency', 'EUR')
            
            # Call API for conversion
            api_key = settings.EXCHANGE_RATE_API_KEY
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}/{amount}"
            
            response = requests.get(url)
            data = response.json()
            
            if data.get('result') == 'success':
                result = {
                    'amount': amount,
                    'from_currency': from_currency,
                    'to_currency': to_currency,
                    'converted_amount': data.get('conversion_result'),
                    'rate': data.get('conversion_rate')
                }
            else:
                error = data.get('error-type', 'An unknown error occurred')
                
        except Exception as e:
            error = f"Error: {str(e)}"
    
    context = {
        'currencies': currencies,
        'amount': amount,
        'from_currency': from_currency,
        'to_currency': to_currency,
        'result': result,
        'error': error
    }
    
    return render(request, 'currency/converter.html', context)

def get_exchange_rate(request):
    """
    API endpoint to get exchange rate for AJAX calls
    """
    if request.method == "GET":
        from_currency = request.GET.get('from_currency')
        to_currency = request.GET.get('to_currency')
        
        if not from_currency or not to_currency:
            return JsonResponse({'error': 'Both currencies are required'}, status=400)
        
        try:
            # Call API for exchange rate
            api_key = settings.EXCHANGE_RATE_API_KEY
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}"
            
            response = requests.get(url)
            data = response.json()
            
            if data.get('result') == 'success':
                return JsonResponse({
                    'rate': data.get('conversion_rate'),
                    'last_updated': data.get('time_last_update_utc')
                })
            else:
                return JsonResponse({'error': data.get('error-type', 'API error')}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)