from django.urls import path
from bbapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('messaging/', views.messaging, name='messaging'),
    path('signup/', views.signup, name="signup"),
    path('profile/', views.createprofile, name="profile"),
    path('login', views.userLog, name="login"),
    path('land', views.home, name="land")
]
