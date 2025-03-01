from django.shortcuts import render
import requests
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def translate_page(request):
    """
    Render the translator page with language options
    """
    # List of common languages for the dropdowns
    languages = [
        {"code": "en", "name": "English"},
        {"code": "es", "name": "Spanish"},
        {"code": "fr", "name": "French"},
        {"code": "de", "name": "German"},
        {"code": "it", "name": "Italian"},
        {"code": "pt", "name": "Portuguese"},
        {"code": "ru", "name": "Russian"},
        {"code": "zh", "name": "Chinese (Simplified)"},
        {"code": "ja", "name": "Japanese"},
        {"code": "ko", "name": "Korean"},
        {"code": "ar", "name": "Arabic"},
        {"code": "hi", "name": "Hindi"},
        {"code": "th", "name": "Thai"},
        {"code": "vi", "name": "Vietnamese"},
        {"code": "nl", "name": "Dutch"},
    ]
    
    context = {
        'languages': languages,
    }
    
    # Handle translation request if form is submitted
    if request.method == 'POST':
        text = request.POST.get('text', '')
        source_lang = request.POST.get('source_language', 'auto')
        target_lang = request.POST.get('target_language', 'en')
        
        if text:
            try:
                # Call Google Translate API
                translation = translate_text(text, source_lang, target_lang)
                
                context.update({
                    'text': text,
                    'source_language': source_lang,
                    'target_language': target_lang,
                    'translation': translation,
                })
            except Exception as e:
                context.update({
                    'text': text,
                    'source_language': source_lang,
                    'target_language': target_lang,
                    'error': str(e),
                })
    
    return render(request, 'translate/translator.html', context)

@csrf_exempt
def translate_api(request):
    """
    API endpoint for AJAX translation requests
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            source_lang = data.get('source_language', 'auto')
            target_lang = data.get('target_language', 'en')
            
            if not text:
                return JsonResponse({'error': 'Text is required'}, status=400)
                
            translation = translate_text(text, source_lang, target_lang)
            
            return JsonResponse({
                'translation': translation,
                'source_language': source_lang,
                'target_language': target_lang
            })
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def translate_text(text, source_language='auto', target_language='en'):
    """
    Translate text using Google Translate API
    """
    api_key = settings.GOOGLE_TRANSLATE_API_KEY
    
    url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"
    
    payload = {
        'q': text,
        'target': target_language,
    }
    
    # Add source language if it's not set to auto
    if source_language != 'auto':
        payload['source'] = source_language
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    
    if 'error' in result:
        raise Exception(result['error']['message'])
    
    # Extract translation from response
    translation = result['data']['translations'][0]['translatedText']
    
    return translation

def detect_language(request):
    """
    API endpoint to detect the language of provided text
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            
            if not text:
                return JsonResponse({'error': 'Text is required'}, status=400)
                
            api_key = settings.GOOGLE_TRANSLATE_API_KEY
            url = f"https://translation.googleapis.com/language/translate/v2/detect?key={api_key}"
            
            payload = {
                'q': text
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, json=payload, headers=headers)
            result = response.json()
            
            if 'error' in result:
                raise Exception(result['error']['message'])
            
            # Extract detected language
            language = result['data']['detections'][0][0]['language']
            confidence = result['data']['detections'][0][0]['confidence']
            
            return JsonResponse({
                'language': language,
                'confidence': confidence
            })
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)