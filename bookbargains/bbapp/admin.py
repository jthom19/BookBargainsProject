from django.contrib import admin
from .models import Profile, Book, Message, Cart, CartItem

# Register your models here.
admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(Message)
admin.site.register(CartItem)
admin.site.register(Cart)