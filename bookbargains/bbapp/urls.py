from django.urls import path
from bbapp import views

urlpatterns = [
    path('', views.hometemp, name='home'),
    path('messaging/', views.messaging, name='messaging'),
    path('signup/', views.signup, name="signup"),
    path('profile/', views.createprofile, name="profile"),
    path('login', views.userLog, name="login"),
    path('land', views.hometemp, name="land"),
    path('listnew', views.createlisting, name="newlisting"), #already linked to see new listing
    path('buyList', views.buyList, name="buyList")
]
