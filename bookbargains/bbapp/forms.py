from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .models import Book

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {
            "username": "Email",
        }

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'major': forms.TextInput(attrs={'class':'form-control'}),
            'housing': forms.TextInput(attrs={'class':'form-control'}),
        }

class ListBookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('user',)
