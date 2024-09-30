from django.urls import path
from .views import map_views, users_views, search_views
from django.contrib.auth import views as auth_views
from django.contrib import messages

urlpatterns = [
    path('register/', users_views.register, name='register'),
    path('login/', users_views.login, name='login'),
    path('', users_views.landingPage, name='landingPage'),  # Homepage
    path('dashboard/', users_views.dashboard, name='dashboard'), #dashboard
    path('logout/', auth_views.LogoutView.as_view(next_page='landingPage'), name='logout'),
    path('explore/', map_views.ExploreMap.as_view(), name='explore'),
    path('search/', search_views.search_restaurants, name='search_restaurants'),
    path('reset_password/', users_views.reset_password, name='reset_password'),
    path('get_security_question/', users_views.get_security_question, name='get_security_question'),
    path('favorites/', search_views.favorites_list, name='favorites_list'),
    path('add_to_favorites/', search_views.add_to_favorites, name='add_to_favorites'),
]