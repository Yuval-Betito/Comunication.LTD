from django.shortcuts import render, redirect
from django.contrib import messages
from utils.password_config import PASSWORD_CONFIG
from .forms import CustomerForm
from django.contrib.auth import  login
from .models import PasswordResetToken, User
from utils.password_utils import validate_password, hash_password
from django.urls import reverse
import hashlib
import os
from .models import PasswordHistory
from django.contrib.auth.decorators import login_required
from .models import Customer
import re
from django.utils.html import escape


def home(request):
    return render(request, 'home.html')

def login_user(request):
    if request.method == 'POST':
        username = escape(request.POST['username'].strip())
        password = request.POST['password'].strip()

        try:
            user = User.objects.get(username=username)


            if user.login_attempts >= PASSWORD_CONFIG['max_login_attempts']:
                messages.error(request, "Your account is locked due to too many failed login attempts. Please try again later.")
                return redirect('login')

            if user.check_password(password):
                user.login_attempts = 0
                user.save()
                login(request, user)
                messages.success(request, "Logged in successfully.")
                return redirect('user_home')
            else:
                user.login_attempts += 1
                user.save()
                messages.error(request, "Invalid credentials.")
        except User.DoesNotExist:
            messages.error(request, "User not found.")
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = escape(request.POST['username'].strip())
        email = escape(request.POST['email'].strip())
        password = request.POST['password'].strip()
        confirm_password = request.POST['confirm_password'].strip()


        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')


        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            messages.error(request, "Username can only contain letters, numbers, and underscores.")
            return redirect('register')


        if User.objects.filter(username=username).exists():
            messages.error(request, "This username is already taken.")
            return redirect('register')


        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect('register')


        password_errors = validate_password(password)
        if password_errors:
            for error in password_errors:
                messages.error(request, error)
            return redirect('register')


        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'register.html')


@login_required
def user_home(request):
    return render(request, 'user_home.html')

@login_required
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            messages.success(request, "Customer added successfully.")
            return redirect('create_customer')
        else:
            messages.error(request, "Failed to create customer. Please fix the errors below.")
    else:
        form = CustomerForm()
    return render(request, 'create_customer.html', {'form': form})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)

            token = hashlib.sha1(os.urandom(64)).hexdigest()
            PasswordResetToken.objects.create(user=user, token=token)


            reset_url = request.build_absolute_uri(reverse('reset_password', args=[token]))
            user.email_user(
                subject="Password Reset",
                message=f"Click the link to reset your password: {reset_url}",
            )
            messages.success(request, "A password reset email has been sent.")
            return redirect('reset_password', token=token)
        except User.DoesNotExist:
            messages.error(request, "No user found with that email address.")
            return redirect('forgot_password')

    return render(request, 'forgot_password.html')


def reset_password(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        if not reset_token.is_valid():
            messages.error(request, "The reset token has expired.")
            return redirect('forgot_password')
    except PasswordResetToken.DoesNotExist:
        messages.error(request, "Invalid reset token.")
        return redirect('forgot_password')

    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password', token=token)


        password_errors = validate_password(password, reset_token.user)
        if password_errors:
            for error in password_errors:
                messages.error(request, error)
            return redirect('reset_password', token=token)


        reset_token.user.set_password(password)
        reset_token.user.save()


        PasswordHistory.objects.create(user=reset_token.user, password=reset_token.user.password)


        reset_token.delete()

        messages.success(request, "Your password has been reset successfully.")
        return redirect('login')

    return render(request, 'reset_password.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']


        if not request.user.check_password(current_password):
            messages.error(request, "The current password is incorrect.")
            return redirect('change_password')


        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('change_password')


        password_errors = validate_password(new_password, user=request.user)
        if password_errors:
            for error in password_errors:
                messages.error(request, error)
            return redirect('change_password')


        request.user.set_password(new_password)
        request.user.save()


        from users.models import PasswordHistory
        PasswordHistory.objects.create(user=request.user, password=hash_password(new_password))

        messages.success(request, "Password changed successfully.")
        return redirect('user_home')

    return render(request, 'change_password.html')



@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})
