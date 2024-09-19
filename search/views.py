from django.shortcuts import render
import requests
from .forms import SearchForm

def search_restaurants(request):
    google_api_key = "AIzaSyA-gA_urq6wnjISp4aHa2IOhHJTu1my-EM"  # Replace with your actual API key
    form = SearchForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # Get the search inputs from the form
        name = form.cleaned_data.get('name')
        cuisine = form.cleaned_data.get('cuisine')
        location = form.cleaned_data.get('location')

        # Default values for latitude and longitude (if no location is provided)
        latitude, longitude = None, None

        # If location is provided, use Geocoding API to get coordinates
        if location:
            geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
            geocode_params = {
                'address': location,
                'key': google_api_key
            }
            geocode_response = requests.get(geocode_url, params=geocode_params)
            geocode_data = geocode_response.json()

            # Debugging: Print the Geocoding API response
            print("Geocoding API Response:", geocode_data)

            status = geocode_data.get('status')
            if status == 'OK' and geocode_data.get('results'):
                location_data = geocode_data['results'][0]['geometry']['location']
                latitude = location_data['lat']
                longitude = location_data['lng']
            else:
                # Extract and display the error message from the Geocoding API response
                error_message = geocode_data.get('error_message', 'Invalid location or address not found')
                return render(request, 'search/search.html', {'form': form, 'error': error_message})

        # Default to the center of Atlanta if no location provided
        if not latitude or not longitude:
            # Latitude and longitude for the center of Atlanta
            latitude, longitude = 33.7490, -84.3880  # Atlanta coordinates

        # Places API Request (Dynamically constructed)
        places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places_params = {
            'location': f"{latitude},{longitude}",
            'radius': 5000,  # Search within 5km by default
            'type': 'restaurant',
            'key': google_api_key
        }

        # Optional search filters: name and cuisine
        if name:
            places_params['keyword'] = name  # Filter by restaurant name
        if cuisine:
            places_params['keyword'] = cuisine  # Filter by cuisine type (e.g., "Italian")

        # Make the Places API request
        places_response = requests.get(places_url, params=places_params)
        places_data = places_response.json()

        # Get the list of restaurants
        restaurants = places_data.get('results', [])

        # Pass the results to the template
        return render(request, 'search/search.html', {'form': form, 'restaurants': restaurants})

    # Initial page load or invalid form submission
    return render(request, 'search/search.html', {'form': form})

