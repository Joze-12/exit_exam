from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import *
from .backends import CustomBackend

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
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user:
                if user.is_student() and not user.studentprofile.approved:
                    return redirect('need_approved')
                elif user.is_student() and user.studentprofile.rejected:
                    return redirect('not_accepted')
                elif not user.is_active:
                    return redirect('inactive_user')
                elif not user.password_changed:
                    return redirect('change_password')
                else:
                    login(request, user)
                    return redirect('dashboard_url')  # Redirect to the dashboard or home page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})

def dashboard_render(request):
    return render(request, "dashboard.html")



def student_signup_view(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            # Save the user with the student role
            user = form.save(commit=False)
            user.role = User.Role.STUDENT
            user.save()

            # Create the associated StudentProfile instance
            student_id = form.cleaned_data['student_id']
            department = form.cleaned_data['department']
            program = form.cleaned_data['program']

            StudentProfile.objects.create(
                user=user,
                student_id=student_id,
                department=department,
                program=program,
            )

            # Redirect to a success page
            return redirect('login')
    else:
        form = StudentSignupForm()

    return render(request, 'auth/student_signup.html', {'form': form})



