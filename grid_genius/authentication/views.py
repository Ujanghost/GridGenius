from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
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
            form.save()
            messages.success(request, 'Sign up successful. You can now log in.')
            return redirect('login')
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
                return redirect('home')  # Redirect to a homepage or dashboard after login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})



# Add other views as needed
def contact_view(request):
    return render(request, 'contact.html')

def service_view(request):
    return render(request, 'service.html')

def portfolio_view(request):
    return render(request, 'portfolio.html')