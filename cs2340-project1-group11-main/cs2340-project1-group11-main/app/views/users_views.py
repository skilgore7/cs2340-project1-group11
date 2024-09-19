from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import login, authenticate
from django.contrib import messages
from ..forms import UserRegisterForm
from django.contrib.auth.decorators import login_required


def landingPage(request):
    return render(request, 'app/landingPage.html')

# Register view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {'form': form})

# Login view
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'app/dashboard.html', {'username': request.user.username})
