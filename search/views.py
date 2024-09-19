
# search/views.py

import requests
from django.shortcuts import render
from django.conf import settings
from .forms import SearchForm
from geopy.distance import geodesic

# Function to calculate distance between two locations
def calculate_distance(user_location, restaurant_location):
    return geodesic(user_location, restaurant_location).meters

def search_restaurants(request):
    form = SearchForm()
    restaurants = []

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data.get('name', '')
            cuisine = form.cleaned_data.get('cuisine', '')
            location = form.cleaned_data['location']
            min_rating = form.cleaned_data.get('min_rating', 0)
            max_distance = form.cleaned_data.get('max_distance', 5000)  # Default 5000 meters

            # Get latitude and longitude from location (using Google Geocoding API)
            google_api_key = settings.GOOGLE_API_KEY
            geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"

            geocode_params = {
                'address': location,
                'key': google_api_key
            }
            # After making the API request:
            geocode_response = requests.get(geocode_url, params=geocode_params)
            print(geocode_response.status_code)  # Should return 200 if successful
            print(geocode_response.json())  # Print the API response to check for any errors

            geocode_response = requests.get(geocode_url, params=geocode_params)
            geocode_data = geocode_response.json()

            if geocode_data['results']:
                lat_lng = geocode_data['results'][0]['geometry']['location']
                latitude = lat_lng['lat']
                longitude = lat_lng['lng']

                # Search restaurants using Google Places API
                places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                places_params = {
                    'location': f"{latitude},{longitude}",
                    'radius': max_distance,
                    'type': 'restaurant',
                    'keyword': f"{name} {cuisine}",
                    'key': google_api_key
                }

                places_response = requests.get(places_url, params=places_params)
                places_data = places_response.json()

                restaurants = places_data.get('results', [])

                if places_data.get('results'):
                    restaurants = places_data['results']

                    # Filter by rating
                    restaurants = [r for r in restaurants if r.get('rating', 0) >= min_rating]

                    # Calculate distance from user location
                    for restaurant in restaurants:
                        restaurant_location = (
                            restaurant['geometry']['location']['lat'],
                            restaurant['geometry']['location']['lng']
                        )
                        user_location = (latitude, longitude)
                        restaurant['distance'] = calculate_distance(user_location, restaurant_location)

    return render(request, 'search/search.html', {'form': form, 'restaurants': restaurants})
