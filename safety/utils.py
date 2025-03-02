import urllib.parse
import anthropic
from django.conf import settings

def get_country_safety_info(country_name):
    """Generate safety information for a country using Claude API."""
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    prompt = f"""
    Provide comprehensive safety information for travelers going to {country_name}.
    Format your response as JSON with the following structure:
    {{
        "safety_summary": "Overall safety assessment for the country (2-3 paragraphs)",
        "women_safety_info": "Safety information specifically for women travelers (1-2 paragraphs)",
        "night_safety_info": "Safety information about nighttime travel (1-2 paragraphs)",
        "solo_traveler_info": "Information for solo travelers (1-2 paragraphs)",
        "crime_info": "Common crimes and scams to be aware of (2-3 paragraphs)",
        "transportation_safety_info": "Safety of public transportation (1 paragraph)",
        "emergency_numbers": "List of emergency contact numbers"
    }}
    Don't include any text outside of this JSON structure.
    """
    
    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            temperature=0.2,
            system="You are a helpful travel safety assistant providing factual information in clean JSON format with no markdown formatting or extra text.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        content = response.content[0].text
        
        # Clean up the response and extract JSON
        import json
        import re
        
        # Remove any markdown code block formatting
        content = re.sub(r'```json|```', '', content).strip()
        
        # Try to parse the JSON
        try:
            safety_info = json.loads(content)
            return safety_info
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            # If JSON parsing fails, try to extract the individual fields
            safety_info = {}
            
            # Extract each field using regex
            patterns = {
                'safety_summary': r'"safety_summary":\s*"([^"]+)"',
                'women_safety_info': r'"women_safety_info":\s*"([^"]+)"',
                'night_safety_info': r'"night_safety_info":\s*"([^"]+)"',
                'solo_traveler_info': r'"solo_traveler_info":\s*"([^"]+)"',
                'crime_info': r'"crime_info":\s*"([^"]+)"',
                'transportation_safety_info': r'"transportation_safety_info":\s*"([^"]+)"',
                'emergency_numbers': r'"emergency_numbers":\s*"([^"]+)"'
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, content)
                if match:
                    safety_info[key] = match.group(1)
                else:
                    safety_info[key] = f"No information available about {key.replace('_', ' ')} for {country_name}"
                    
            return safety_info
    
    except Exception as e:
        print(f"Error getting safety info for {country_name}: {str(e)}")
        return None
    
