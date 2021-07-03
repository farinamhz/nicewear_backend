from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField


# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role_choices = ((1, "User"), (2, "Seller"))
    role = models.IntegerField(choices=role_choices, default=1)
    credit = models.IntegerField(blank=False, default=1000000)


class Phone(models.Model):
    phone = PhoneField(
        unique=True,
        error_messages={
            'unique': "A user with this phone already exists."
        }
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Address(models.Model):
    about = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=15)