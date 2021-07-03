from django.db import models
from accounts.models import User, Address, Phone


# Create your models here.


class MainOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    receive_date = models.DateTimeField()
    # status_choices = ((1, "Pending"), (2, "Finished"))
    # status = models.IntegerField(choices=status_choices, default=1)


class Category(models.Model):
    name = models.CharField(max_length=50)


class Product(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=10)
    subtitle = models.CharField(max_length=100)
    color1 = models.CharField(max_length=20)
    color2 = models.CharField(max_length=20)
    color3 = models.CharField(max_length=20)
    category1 = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category1')
    category2 = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category2')
    price = models.PositiveIntegerField(default=0, blank=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(null=False, upload_to="product_picture")
    count_seen = models.PositiveIntegerField(default=0, blank=False)

    def get_str_picture(self):
        if self.picture:
            return str(self.picture.url)
        else:
            return None


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    sub_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField(blank=False)


class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class OrderList(models.Model):
    order = models.ForeignKey(OrderProduct, on_delete=models.CASCADE)
    main_order = models.ForeignKey(MainOrder, on_delete=models.CASCADE)
