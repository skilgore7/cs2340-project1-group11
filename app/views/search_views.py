from django.shortcuts import render
import requests
from ..forms import SearchForm
from django.conf import settings
from ..models import Restaurant, Favorite
#Now need to import necessary features for when people are not authenticated (redirection, 404, etc)
from django.contrib.auth.decorators import login_required #make sure only users who are authenticated can access this
from django.http import HttpResponseRedirect

from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages



def search_restaurants(request):
    google_api_key = "AIzaSyA-gA_urq6wnjISp4aHa2IOhHJTu1my-EM"  # Replace with your actual API key
    key = settings.GOOGLE_API_KEY
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
                'key': key
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
                return render(request, 'app/search.html', {'form': form, 'error': error_message})

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
            'key': key
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
        return render(request, 'app/search.html', {'form': form, 'restaurants': restaurants})

    # Initial page load or invalid form submission
    return render(request, 'app/search.html', {'form': form})

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'app/favorites.html', {'favorites': favorites})

@login_required
def add_to_favorites(request):
    #"Favorite" button will pass these fields through a request
    if request.method == 'POST':
        place_id = request.POST.get('place_id')
        name = request.POST.get('name')
        address = request.POST.get('address')
        rating = request.POST.get('rating')

        # Check if the restaunt is already in database to prevent duplicates
        restaurant, created = Restaurant.objects.get_or_create(
            place_id=place_id,
            defaults={
                'name': name,
                'address': address,
                'rating': rating,
            }
        )

        # Add to favorites
        Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def remove_from_favorites(request):
    if request.method == 'POST':
        place_id = request.POST.get('place_id')
        
        if not place_id:
            print("ERROR: No restaurant specified")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            
        try:
            # Retrieve the Restaurant object based on place_id
            restaurant = Restaurant.objects.get(place_id=place_id)
            
            # Retrieve the Favorite object linking the user and restaurant
            favorite = Favorite.objects.get(user=request.user, restaurant=restaurant)
            
            # Delete the Favorite object
            favorite.delete()
            
            messages.success(request, f"Removed '{restaurant.name}' from your favorites.")
        except Restaurant.DoesNotExist:
            messages.error(request, "Restaurant does not exist.")
        except Favorite.DoesNotExist:
            messages.error(request, "This restaurant is not in your favorites.")
    else:
        messages.error(request, "Invalid request method.")
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        


