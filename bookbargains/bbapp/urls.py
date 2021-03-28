from django.urls import path
from bbapp import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('messaging', views.messaging, name='messaging')
    path('', home_view, name="home")
    path('signup/', signup_view, name="signup")
]