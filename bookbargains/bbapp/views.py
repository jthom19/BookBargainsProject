from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from .forms import CreateUserForm, CreateProfileForm, ListBookForm, MessageForm
from .models import Book, Cart, Wishlist, Transaction
from .filters import BookFilter
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

#Each time a user is created, a cart and wishlist are also created
@receiver(post_save, sender=User)
def createcartandwishlist(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(owner=instance)
        Wishlist.objects.create(owner=instance)

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

#This function is called when a user goes to create an account.
def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            raw_password = form.cleaned_data.get('password1')
            raw_email = form.cleaned_data.get('username')
            if 'bc.edu' in raw_email:
                user = form.save()
                user.save()
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                return redirect('../profile/')
            else:
                messages.error(request,"Please enter a valid BC email.")
                return redirect('signup')
    else:
        form = CreateUserForm()
    return render(request, 'register.html', {'form': form})

#This function is called when users go to create a profile after first signing up.
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

#This function is called when the user goes to create a book listing. The ISBN number is confirmed.
@login_required
def createlisting(request):
    newlistingform = ListBookForm(initial={'user':request.user})
    if request.method == "POST":
        newlistingform = ListBookForm(request.POST, request.FILES)
        if newlistingform.is_valid():
            isbnone = newlistingform.cleaned_data['ISBN13']
            isbntwo = newlistingform.cleaned_data['ISBN13Conf']
            if (isbnone == isbntwo):
                newlistingform = newlistingform.save(commit=False)
                newlistingform.user = request.user
                newlistingform = newlistingform.save()
                messages.success(request, "Success! Your book has been listed!")
                return redirect('../')
            else:
                messages.error(request, "Make sure ISBN13 fields match.")
                return redirect('newlisting')
    return render(request, 'sellerListing.html', {'ListBookForm':ListBookForm})

#This function is related to viewing all available books and filtering based on user input.
@login_required
def searchbooks(request):
    allbooks = Book.objects.all()
    myFilter = BookFilter(request.GET, queryset=allbooks)
    allbooks = myFilter.qs
    context = {'books':allbooks,'filter': myFilter}
    return render(request, 'searchfilter.html', context)

@login_required
def createmessage(request):
    newmessageform = MessageForm()
    if request.method == "POST":
        newmessageform = MessageForm(request.POST)
        if newmessageform.is_valid():
            newmessageform = newmessageform.save()
        return redirect('../')
    return render(request, 'messages.html', {'MessageForm':MessageForm})

#This function is called when the user goes to message the user from the cart. It will create a transaction instance.
@login_required
def createtransaction(request, bookid):
    newtransaction = Transaction.objects.create(buyer=request.user, book=Book.objects.get(uuid=bookid), seller=Book.objects.get(uuid=bookid).user)
    return redirect('home')


##These functions are related to the cart and wishlist:
    #adding to cart
    #adding to wishlist
    #changing from wishlist to cart
    #viewing wishlist
    #viewing cart

@login_required
def addtocart(request, bookid):
    booktoadd = Book.objects.get(uuid=bookid)
    cart, created = Cart.objects.get_or_create(owner=request.user)
    cart.cartitem.add(booktoadd)
    cart.save()
    messages.success(request, "Success! A book has been added to the cart!")
    return redirect('search')

@login_required
def addtowishlist(request, bookid):
    booktoadd = Book.objects.get(uuid=bookid)
    wishlist, created = Wishlist.objects.get_or_create(owner=request.user)
    wishlist.item.add(booktoadd)
    wishlist.save()
    messages.success(request, "Success! A book has been added to your wishlist!")
    return redirect('search')

@login_required
def viewcart(request):
    currentcart = Cart.objects.get(owner=request.user)
    context = {'cart': currentcart}
    return render(request, 'cart.html', context)

@login_required
def viewwishlist(request):
    currentwishlist = Wishlist.objects.get(owner=request.user)
    context = {'wishlist': currentwishlist}
    return render(request, 'wishlist.html', context)

@login_required
def switchfromwishlisttocart(request, bookid):
    booktoswitch = Book.objects.get(uuid=bookid)
    currentwishlist = Wishlist.objects.get(owner = request.user)
    currentcart = Cart.objects.get(owner = request.user)
    currentwishlist.item.remove(booktoswitch)
    currentcart.cartitem.add(booktoswitch)
    messages.success(request, "Success! A book from your wishlist has been added to your cart.")
    return redirect('wishlist')

@login_required
def removefromcart(request, bookid):
    booktoremove = Book.objects.get(uuid=bookid)
    cart, created = Cart.objects.get_or_create(owner=request.user)
    cart.cartitem.remove(booktoremove)
    cart.save()
    messages.success(request, "Success! A book has been removed from your cart!")
    return redirect('cart')

@login_required
def removefromwishlist(request, bookid):
    booktoremove = Book.objects.get(uuid=bookid)
    wishlist, created = Wishlist.objects.get_or_create(owner=request.user)
    wishlist.item.remove(booktoremove)
    wishlist.save()
    messages.success(request, "Success! A book has been removed from your wishlist!")
    return redirect('wishlist')

#These two functions have to deal with the user viewing their own book listings and removing if necessary.
@login_required
def viewmybooks(request):
    mycurrentbooks = Book.objects.filter(user = request.user)
    context = {'mycurrentbooks':mycurrentbooks}
    return render(request, 'mybooks.html', context)

@login_required
def removelisting(request, bookid):
    booktoremove = Book.objects.get(uuid=bookid)
    booktoremove.delete()
    messages.success(request, "Your book has been successfully removed from listings. ")
    return redirect('mybooks')
