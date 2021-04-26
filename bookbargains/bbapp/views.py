from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CreateUserForm, CreateProfileForm, ListBookForm, MessageForm
from django.views.generic import TemplateView, ListView
from .models import Book, Cart
from django.db.models import Q
# Create your views here.


def userLog(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'signup.html')

def messaging(request):
    return render(request, 'messaging.html')

def hometemp(request):
    return render(request, 'hometemp.html')

def buyList(request):
    return render(request, 'buyerListing.html')

def logoutuser(request):
    logout(request)
    return redirect('../')

class HomePageView(ListView):
    model = Book
    template_name= 'search.html'

class SearchResultsView(ListView):
    model = Book
    template_name = 'searchresults.html'
    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(
                ISBN13__icontains=query) | Q(edition__icontains=query) | Q(
                    condition__icontains=query) | Q(field__icontains=query))
        return object_list

def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('../profile/')
    else:
        form = CreateUserForm()
    return render(request, 'register.html', {'form': form})

def createprofile(request):
    p_form = CreateProfileForm(initial={'user':request.user})
    if request.method == "POST":
        p_form = CreateProfileForm(request.POST)
        if p_form.is_valid():
            Profile = p_form.save(commit=False)
            Profile.user = request.user
            Profile = p_form.save()
            User = request.user
            User.save()
            cleanfirstname = p_form.cleaned_data.get('first_name')
            cleanlastname = p_form.cleaned_data.get('last_name')
            User.first_name = cleanfirstname
            User.last_name = cleanlastname
            User.email = User.username
            User.save()
            return redirect('../')
        else:
            form = CreateProfileForm()
    return render(request, 'createprofile.html', {'p_form':p_form})

def createlisting(request):
    newlistingform = ListBookForm(initial={'user':request.user})
    if request.method == "POST":
        newlistingform = ListBookForm(request.POST, request.FILES)
        if newlistingform.is_valid():
            newlistingform = newlistingform.save(commit=False)
            newlistingform.user = request.user
            newlistingform = newlistingform.save()
        return redirect('../')
    return render(request, 'sellerListing.html', {'ListBookForm':ListBookForm})

def createmessage(request):
    newmessageform = MessageForm()
    if request.method == "POST":
        newmessageform = MessageForm(request.POST)
        if newmessageform.is_valid():
            newmessageform = newmessageform.save()
        return redirect('../')
    return render(request, 'messages.html', {'MessageForm':MessageForm})

def viewcart(request):
    allcarts= Cart.objects.filter(owner=request.user)
    context= {'allcarts': allcarts}
    return render(request, 'cart.html', context)