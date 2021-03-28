from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
# Create your views here.


def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'signup.html')

def messaging(request):
    return render(request, 'messaging.html')

def home_view(request):
    return render(request, 'LandingPage.html')

def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('LandingPage')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})