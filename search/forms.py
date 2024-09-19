
from django import forms

class SearchForm(forms.Form):
    name = forms.CharField(label="Restaurant Name", required=False, max_length=100)
    cuisine = forms.CharField(label="Cuisine", required=False, max_length=100)
    location = forms.CharField(label="Location", required=True, max_length=100)
    min_rating = forms.FloatField(label="Minimum Rating (1-5)", required=False)
    max_distance = forms.IntegerField(label="Maximum Distance (meters)", required=False)
