from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


class Profile(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE) #User deleted? Delete profile
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length = 100, null=True)
    phone = models.CharField(max_length = 10, null=True)
    major = models.CharField(max_length = 100, null=True)
    housing = models.CharField(max_length = 100, null=True)

    def __str__(self):
        return self.user.username


