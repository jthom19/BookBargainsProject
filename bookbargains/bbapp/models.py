from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 150)
    phone = models.CharField(max_length = 10)
    major = models.CharField(max_length = 100)
    housing = models.CharField(max_length = 100)

    def __str__(self):
        return self.user.username


class Classes(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    classes = models.CharField(max_length=200)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)
