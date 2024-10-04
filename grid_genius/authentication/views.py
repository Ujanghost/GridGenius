from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, LoginForm


@login_required
def home(request):
    return render(request,'home.html',{})

# About view
def about_view(request):
    return render(request, 'about.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Check if a user with the same email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists. Please try another one.')
                return redirect('authentication:signup')

            # If no duplicate email, save the form
            form.save()
            messages.success(request, 'Sign up successful. You can now log in.')
            return redirect('authentication:login')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')  # Success message
                return redirect('authentication:home')  # Redirect to a homepage or dashboard after login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

# View for logging out
def logout_view(request):
    logout(request)
    return redirect('authentication:login')  # Redirect to login page after logout



# Add other views as needed
def contact_view(request):
    return render(request, 'contact.html')

def service_view(request):
    return render(request, 'service.html')

def portfolio_view(request):
    return render(request, 'portfolio.html')