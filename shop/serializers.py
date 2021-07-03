from . import models
from rest_framework import serializers


# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Order
#         fields = "__all__"
#         # read_only_fields = 'created_date'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"
        # read_only_fields = 'count_seen'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubCategory
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderProduct
        fields = "__all__"


class MainOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MainOrder
        fields = "__all__"


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderList
        fields = "__all__"