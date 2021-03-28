from django.urls import path
from bbapp import views

urlpatterns = [
    path('login', views.userLog, name='login'),
    path('register', views.register, name='register'),
    path('messaging', views.messaging, name='messaging'),
<<<<<<< HEAD
    path('', views.home_view, name="home"),
    path('signup/', views.signup_view, name="signup"),
=======
    path('', views.home, name="home"),
    path('signup/', views.signup_view, name="signup")
>>>>>>> 08d6f3ffeda71323a860968311362a702208d71f
]