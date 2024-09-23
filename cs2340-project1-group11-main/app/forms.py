from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SearchForm(forms.Form):
    name = forms.CharField(label="Restaurant Name", required=False, max_length=100)
    cuisine = forms.CharField(label="Cuisine", required=False, max_length=100)
    location = forms.CharField(label="Location", required=True, max_length=100)
    min_rating = forms.FloatField(label="Minimum Rating (1-5)", required=False)
    max_distance = forms.IntegerField(label="Maximum Distance (meters)", required=False)
