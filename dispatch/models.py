from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django_extensions.db.models import TimeStampedModel

from dispatchproject import settings


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    otp = models.CharField(max_length=4, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email


class Order(TimeStampedModel):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    shipper = models.CharField(max_length=100)
    pickup = models.DateTimeField(auto_now_add=True)
    delivery = models.DateTimeField(auto_now_add=True)


class Dispatch(TimeStampedModel):
    Action = (
        ('P', 'Pickup'),
        ('D', 'Delivery'),
    )
    Status = (
        ('P', 'Pending'),
        ('I', 'in-transit'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    file = models.FileField(max_length=None, default='')
    action = models.CharField(max_length=120, choices=Action, default='Pickup')
    arrival_date = models.DateTimeField(auto_now=True, null=True)
    departure_date = models.DateTimeField(auto_now=True, null=True)
    arrived = models.BooleanField(default=False)
    departed = models.BooleanField(default=False)
    status = models.CharField(max_length=120, choices=Status, default='pending')
