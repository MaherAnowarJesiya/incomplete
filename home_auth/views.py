from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.crypto import get_random_string
from .models import PasswordResetRequest  # Assuming this is a custom model you've created


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        # Create the user (note: default User model has no role field)
        user = User.objects.create_user(
            username=email,  # Required field
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        # Add role-specific logic (requires extending the User model or using a profile model)
        if role == 'student':
            user.profile.role = 'student'
        elif role == 'teacher':
            user.profile.role = 'teacher'
        elif role == 'admin':
            user.profile.role = 'admin'

        user.save()
        login(request, user)
        messages.success(request, 'Signup Successful!')
        return redirect('index')

    return render(request, 'authentication/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            role = user.profile.role  # Assuming role is stored in a related profile model

            if role == 'admin':
                return redirect("admin_dashboard")
            elif role == 'teacher':
                return redirect("teacher_dashboard")
            elif role == 'student':
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid user role')
                return redirect('index')
        else:
            messages.error(request, 'Invalid Credentials')

    return render(request, 'authentication/login.html')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()

        if user:
            token = get_random_string(32)
            reset_request = PasswordResetRequest.objects.create(user=user, email=email, token=token)
            reset_request.send_reset_email()
            messages.success(request, 'Reset link sent to your email.')
        else:
            messages.error(request, 'Email not found')

    return render(request, 'authentication/forgot-password.html')


def reset_password_view(request, token):
    reset_request = PasswordResetRequest.objects.filter(token=token).first()

    if not reset_request or not reset_request.is_valid():
        messages.error(request, "Invalid or expired reset link")
        return redirect('index')

    if request.method == 'POST':
        new_password = request.POST['new_password']
        reset_request.user.set_password(new_password)
        reset_request.user.save()
        messages.success(request, 'Password reset successful')
        return redirect('login')

    return render(request, 'authentication/reset_password.html', {'token': token})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')
