from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Sum
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE) #User deleted? Delete profile
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length = 100, null=True)
    phone = models.CharField(max_length = 10, null=True)
    major = models.CharField(max_length = 100, null=True)
    housing = models.CharField(max_length = 100, null=True)
    def __str__(self):
        return self.user.username

class Rating(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    rating = models.DecimalField(decimal_places=2, max_digits=5, default=5.00)
    def __str__(self):
        return str(user.username)+' has a rating of '+rating

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
    ('ACT', 'Accounting'), 
    ('OTH', 'Other'),
    )

SELL_DONATE_CHOICES = (('SO', 'Select One'), ('SE', 'Selling'), ('DO','Donating'))

class Book(models.Model):
    uuid=models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
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
    ISBN13Conf = models.CharField(max_length=13, null=True)
    edition = models.CharField(max_length=100, null=True)
    condition = models.CharField(
        max_length=2,
        choices=BOOK_CONDITION_CHOICES,
        default='Select One',
        null=True)  #dropdown
    field = models.CharField(
        max_length=4, choices=FIELD_CHOICES, default='Select One',
        null=True)  #dropdown
    price = models.DecimalField(max_digits=100, decimal_places=2, null=True)
    def __str__(self):
        return self.title


class Message(models.Model):
    recipient = models.ManyToManyField(User, related_name = 'user')
    sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'sender')
    subject = models.CharField(max_length = 1000, blank = True)
    message = models.TextField()
    sent = models.DateTimeField(auto_now_add = True)
    unread = models.BooleanField(default = True)

    def __str__(self):
        return 'Message from ' + str(self.sender) + '.  Subject:' + str(self.subject)

TRANSACTION_CHOICES = (('In progress', 'In progress'), ('Completed (pending)', 'Completed (pending)'), ('Completed','Completed'))

class Transaction(models.Model):
    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    buyer = models.ForeignKey(User,default = 1,null = True, on_delete = models.SET_NULL,related_name='buyer')
    seller = models.ForeignKey(User,default = 1,null = True, on_delete = models.SET_NULL, related_name='seller')
    book = models.ForeignKey(Book,default = 1,null = True, on_delete = models.SET_NULL, related_name='book')
    status = models.CharField(max_length=40, choices=TRANSACTION_CHOICES, default='In progress', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.uuid

class Cart(models.Model):
    owner = models.OneToOneField(User, on_delete = models.CASCADE, null=True)
    cartitem = models.ManyToManyField(Book)
    @property
    def total(self):
        return self.cartitem.aggregate(Sum('price'))['price__sum'] or 0
    def __str__(self):
        return 'This is the cart for: '+str(self.owner.username)

class Wishlist(models.Model):
    owner = models.OneToOneField(User, on_delete = models.CASCADE, null=True)
    item = models.ManyToManyField(Book)
    @property
    def total(self):
        return self.item.aggregate(Sum('price'))['price__sum'] or 0
    def __str__(self):
        return 'This is the wishlist for: '+str(self.owner.username)