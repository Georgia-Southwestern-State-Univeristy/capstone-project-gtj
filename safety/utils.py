import anthropic
from django.conf import settings

def get_country_safety_info(country_name):
    """
    Generate safety information for a country using Claude API.
    Returns a dictionary of safety information.
    """
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    prompt = f"""
    Provide comprehensive safety information for travelers going to {country_name}.
    Format your response as a structured set of information:

    1. Overall safety summary (2-3 paragraphs)
    2. Women's safety information (1-2 paragraphs)
    3. Night safety information (1-2 paragraphs)
    4. Solo traveler information (1-2 paragraphs)
    5. Crime information and common scams (2-3 paragraphs)
    6. Transportation safety information (1 paragraph)
    7. Emergency numbers and resources

    Base your information on factual travel safety data and provide balanced, practical advice.
    """
    
    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            temperature=0.2,
            system="You are a helpful travel safety assistant providing factual, balanced information about safety for tourists.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        content = response.content[0].text
        
        # Parse the content into sections
        sections = content.split("\n\n")
        
        # Extract the different sections (simplified)
        safety_info = {
            'safety_summary': sections[0] if len(sections) > 0 else "",
            'women_safety_info': sections[1] if len(sections) > 1 else "",
            'night_safety_info': sections[2] if len(sections) > 2 else "",
            'solo_traveler_info': sections[3] if len(sections) > 3 else "",
            'crime_info': sections[4] if len(sections) > 4 else "",
            'transportation_safety_info': sections[5] if len(sections) > 5 else "",
            'emergency_numbers': sections[6] if len(sections) > 6 else "",
        }
        
        return safety_info
    
    except Exception as e:
        print(f"Error getting safety info for {country_name}: {str(e)}")
        return None