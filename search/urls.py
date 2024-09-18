# search/urls.py
#https://chatgpt.com/share/66eb35f5-3d64-800a-9b98-9ddd1d1b9167
from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_restaurants, name='search_restaurants'),
]