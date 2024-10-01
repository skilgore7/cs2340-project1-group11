import requests
from django.conf import settings
from django.shortcuts import render


def restaurant_detail(request, place_id):
    google_api_key = settings.GOOGLE_API_KEY
    places_url = "https://maps.googleapis.com/maps/api/place/details/json"

    # Fetch restaurant details from Google Places API
    params = {
        'place_id': place_id,
        'key': google_api_key
    }

    response = requests.get(places_url, params=params)
    restaurant_data = response.json()

    # Check if the API returned results
    if restaurant_data.get('status') == 'OK':
        restaurant = restaurant_data['result']
    else:
        return render(request, 'app/404.html')  # Handle not found
    cuisine_types = restaurant.get('result', {}).get('types', [])
    formatted_cuisine = ', '.join(cuisine_types)
    context = {
        'restaurant': restaurant,
        'google_api_key': google_api_key,
        'cuisine' : formatted_cuisine,
    }

    return render(request, 'app/restaurant_detail.html', context)

