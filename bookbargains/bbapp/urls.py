from django.urls import path
from django.contrib.auth import views as djangoviews
from bbapp import views
from bbapp.forms import UserLoginForm

urlpatterns = [
    path('', views.hometemp, name='home'),
    path('messaging/', views.messaging, name='messaging'),
    path('signup/', views.signup, name="signup"),
    path('profile/', views.createprofile, name="profile"),
    path('land', views.hometemp, name="land"),
    path('listnew', views.createlisting, name="newlisting"), #already linked to see new listing
    path('buyList', views.buyList, name="buyList"),
    
    path('logout', views.logoutuser, name='logout'),
    path('login',djangoviews.LoginView.as_view(template_name="login.html",authentication_form=UserLoginForm),name='login')
]
