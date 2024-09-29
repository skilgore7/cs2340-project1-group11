# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile  # Ensure this import is correct

SECURITY_QUESTIONS = {
    'favorite_place': 'What is your favorite place in the world?',
    'middle_name': 'What is your middle name?'
}

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    security_question = forms.ChoiceField(choices=[
        ('favorite_place', SECURITY_QUESTIONS['favorite_place']),
        ('middle_name', SECURITY_QUESTIONS['middle_name']),
    ])
    security_answer = forms.CharField(max_length=255, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'security_question', 'security_answer']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Get the selected question text based on the choice made
            question_text = self.cleaned_data['security_question']
            UserProfile.objects.create(
                user=user,
                security_question=SECURITY_QUESTIONS[question_text],  # Use the text here
                security_answer=self.cleaned_data['security_answer']
            )
        return user



class SearchForm(forms.Form):
    name = forms.CharField(label="Restaurant Name", required=False, max_length=100)
    cuisine = forms.CharField(label="Cuisine", required=False, max_length=100)
    location = forms.CharField(label="Location", required=True, max_length=100)
    min_rating = forms.FloatField(label="Minimum Rating (1-5)", required=False)
    max_distance = forms.IntegerField(label="Maximum Distance (meters)", required=False)



