from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'signup.html')

def messaging(request):
    return render(request, 'messaging.html')