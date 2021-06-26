from django.contrib import admin
from .models import OrderProduct, SubCategory, Category, Comment, Product, Order

admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Comment)