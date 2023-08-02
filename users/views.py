from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


def not_accepted_view(request):
    return render(request, "auth/not_accepted.html")

def not_approved_view(request):
    return render(request, "auth/not_approved.html")

def inactive_user_view(request):
    return render(request, "auth/inactive_user.html")

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            user.password_changed = True
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')  # Redirect to the success page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard_url')  # Redirect to the dashboard or home page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm(request)

    return render(request, 'auth/login.html', {'form': form})

def dashboard_render(request):
    return render(request, "dashboard.html")