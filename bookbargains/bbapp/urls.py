from django.urls import path
from bbapp import views

urlpatterns = [
    path('login', views.userLog, name='login'),
    path('register', views.register, name='register'),
    path('messaging', views.messaging, name='messaging'),
    path('', views.home_view, name="home"),
    path('signup/', views.signup_view, name="signup"),
]
