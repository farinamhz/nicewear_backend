from django.db import models
from accounts.models import User, Address


# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    receive_date = models.DateTimeField()


class Product(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)
    price = models.PositiveIntegerField(default=0, blank=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True, upload_to="product_picture")
    count_seen = models.PositiveIntegerField(default=0, blank=False)


class Category(models.Model):
    name = models.CharField(max_length=50)


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    sub_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category')


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
