from django.shortcuts import render, get_object_or_404
import requests
from django.conf import settings


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

    context = {
        'restaurant': restaurant,
    }

    return render(request, 'app/restaurant_detail.html', context)
