from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import messages

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('', views.landingPage, name='landingPage'),  # Homepage
    path('dashboard/', views.dashboard, name='dashboard'), #dashboard
    path('logout/', auth_views.LogoutView.as_view(next_page='landingPage'), name='logout'),
]
