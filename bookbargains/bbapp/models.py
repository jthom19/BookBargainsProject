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


BOOK_CONDITION_CHOICES = (('SO', 'Select One'), ('NE', 'New'), ('GR', 'Great'),
                          ('GO', 'Good'), ('AV', 'Average'), ('PO', 'Poor'))

FIELD_CHOICES = (
    ('SO', 'Select One'),
    ('ART', 'Arts'),
    ('MSC', 'Music'),
    ('HST', 'History'),
    ('LNG', 'Languages'),
    ('LAW', 'Law'),
    ('PHL', 'Philosophy'),
    ('THE', 'Theology'),
    ('ECN', 'Economics'),
    ('PLS', 'Political Science'),
    ('PSY', 'Psychology'),
    ('SOC', 'Sociology'),
    ('NUR', 'Nursing'),
    ('BIO', 'Biology'),
    ('CHM', 'Chemistry'),
    ('PHY', 'Physics'),
    ('ENG', 'Engineering'),
    ('CSC', 'Computer Science'),
    ('MTH', 'Mathematics'),
    ('BUS', 'Business'),
    ('FIN', 'Finance'),
    ('ACT', 'Accounting'), )

SELL_DONATE_CHOICES = (('SO', 'Select One'), ('SE', 'Selling'), ('DO',
                                                                 'Donating'))

class Book(models.Model):
    #need primary key
    user = models.ForeignKey(User,default = 1,null = True, on_delete = models.SET_NULL, blank=False)
    image = models.ImageField(upload_to = 'images/', null=True, blank=False)
    selldonate = models.CharField(
        max_length=2,
        choices=SELL_DONATE_CHOICES,
        default='Select One',
        null=True)
    title = models.CharField(max_length=100, null=True)
    author = models.CharField(max_length=100, null=True)
    ISBN13 = models.CharField(max_length=13, null=True)
    edition = models.CharField(max_length=100, null=True)
    condition = models.CharField(
        max_length=2,
        choices=BOOK_CONDITION_CHOICES,
        default='Select One',
        null=True)  #dropdown
    field = models.CharField(
        max_length=4, choices=FIELD_CHOICES, default='Select One',
        null=True)  #dropdown
    price = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title