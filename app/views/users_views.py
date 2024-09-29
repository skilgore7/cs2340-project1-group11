from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ..forms import UserRegisterForm
from ..models import UserProfile
from django.http import JsonResponse
import json

def landingPage(request):
    return render(request, 'app/landingPage.html')

# Register view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save the user but don't commit to the database yet
            user.save()  # Save the User first

            # Create a UserProfile instance to store the security question and answer
            UserProfile.objects.create(
                user=user,
                security_question=form.cleaned_data['security_question'],
                security_answer=form.cleaned_data['security_answer']
            )

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

# Reset password view
def reset_password(request):
    if request.method == 'POST':
        try:
            if request.headers.get('Content-Type') == 'application/json':
                data = json.loads(request.body)
                username = data.get('username')
                security_answer = data.get('security_answer')
                new_password = data.get('new_password')
            else:
                username = request.POST.get('username')
                security_answer = request.POST.get('security_answer')
                new_password = request.POST.get('new_password')

            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)

            # Check the security answer
            if user_profile.security_answer == security_answer:
                user.set_password(new_password)
                user.save()
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({'success': True})
                else:
                    messages.success(request, 'Your password has been reset successfully.')
                    return redirect('login')
            else:
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({'success': False, 'error': 'Incorrect security answer.'})
                else:
                    messages.error(request, 'Incorrect security answer.')

        except User.DoesNotExist:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'success': False, 'error': 'User does not exist.'})
            else:
                messages.error(request, 'User does not exist.')
        except UserProfile.DoesNotExist:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'success': False, 'error': 'User profile does not exist.'})
            else:
                messages.error(request, 'User profile does not exist.')

    return render(request, 'app/reset_password.html')


def get_security_question(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Load JSON data from the request
        username = data.get('username')

        try:
            user = User.objects.get(username=username)  # Fetch the user by username
            user_profile = UserProfile.objects.get(user=user)  # Get the user profile

            return JsonResponse({'security_question': user_profile.security_question})  # Return the security question
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist.'}, status=404)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile does not exist.'}, status=404)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
def dashboard(request):
    return render(request, 'app/dashboard.html', {'username': request.user.username})



