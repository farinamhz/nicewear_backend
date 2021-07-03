from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from . import serializers
from rest_framework.response import Response
from . import models
from accounts.models import User, Address
from . import permissions
from django.db.models import F
from rest_framework.exceptions import ValidationError


# Create your views here.


class CreateCategory(generics.CreateAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()


class CreateSubCategory(generics.CreateAPIView):
    serializer_class = serializers.SubCategorySerializer
    queryset = models.SubCategory.objects.all()


class CreateComment(generics.CreateAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()


class GetCategories(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


# class GetSubCategories(generics.ListAPIView):
#     queryset = models.Category.objects.all()
#     serializer_class = serializers.CategorySerializer


class GetCategoryById(generics.RetrieveAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get(self, request, *args, **kwargs):
        category_id_list = models.SubCategory.objects.filter(category=self.kwargs['pk']).values_list('sub_category',
                                                                                                     flat=True)
        obj = models.Category.objects.filter(pk__in=category_id_list)
        serializer = self.serializer_class(obj, many=True)
        return Response(serializer.data)


class CreateProduct(generics.CreateAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = (IsAuthenticated,)


class DeleteProduct(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, ]  # + IsOwner
    queryset = models.Product.objects.all()

    def get_queryset(self):
        return models.Product.objects.filter(pk=self.kwargs['pk'], seller=self.request.user)


@api_view(['GET', ])
# @permission_classes((IsAuthenticated, ))
def get_product(request, pk):
    try:
        product = models.Product.objects.get(pk=pk)
        product.count_seen += 1
        product.save()
        prod_ser = serializers.ProductSerializer(product)
        return Response(prod_ser.data, status=status.HTTP_200_OK)

    except models.Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class GetProductByCategory1(generics.RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def get(self, request, *args, **kwargs):
        obj = models.Product.objects.filter(category1__pk=self.kwargs['pk'])
        serializer = self.serializer_class(obj, many=True)
        return Response(serializer.data)


class GetProductByCategories(generics.RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def get(self, request, *args, **kwargs):
        obj = models.Product.objects.filter(category2__pk=self.kwargs['pk2'], category1__pk=self.kwargs['pk1'])
        serializer = self.serializer_class(obj, many=True)
        return Response(serializer.data)


class GetComments(generics.RetrieveAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get(self, request, *args, **kwargs):
        obj = models.Comment.objects.filter(product__pk=self.kwargs['pk'])
        serializer = self.serializer_class(obj, many=True)
        return Response(serializer.data)


class BuyThisProduct(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.OrderProductSerializer
    queryset = models.OrderProduct.objects.all()


#
# class GetProductByCountSeen(generics.RetrieveAPIView):
#     queryset = models.Product.objects.all()
#     serializer_class = serializers.ProductSerializer
#
#     def get(self, request, *args, **kwargs):
#         obj = models.Product.objects.filter(category2__pk=self.kwargs['pk'])
#         serializer = self.serializer_class(obj, many=True)
#         return Response(serializer.data)

# class GetProductById(generics.RetrieveUpdateAPIView):
#     queryset = models.Product.objects.all()
#     serializer_class = serializers.ProductReadSerializer
#     # lookup_field = 'pk'
#     #
#     def get_object(self):
#         pk = self.kwargs["pk"]
#         tr
#         return get_object_or_404(models.Product, pk=pk)


class GetOrders(generics.RetrieveAPIView):
    queryset = models.OrderProduct.objects.all()
    serializer_class = serializers.OrderProductSerializer
    permission_classes = [IsAuthenticated, permissions.IsUser2]

    def get(self, request, *args, **kwargs):
        obj = models.OrderProduct.objects.filter(user__pk=request.user.pk)
        serializer = self.serializer_class(obj, many=True)
        return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def create_main_order(request):
    try:
        user = request.data['user']
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    address = request.data['address']
    receive_date = request.data['receive_date']
    phone = request.data['phone']
    orders_list = request.data['orders_list']
    main_order_context = {
        "user": user,
        "phone": phone,
        "address": address,
        "receive_date": receive_date
    }
    main_order_ser = serializers.MainOrderSerializer(data=main_order_context)
    if main_order_ser.is_valid():
        main_order_ser.save()
        for each_order in orders_list:
            orders_context = {'main_order': main_order_ser.data['id'], 'order': each_order}
            orders_ser = serializers.OrderListSerializer(data=orders_context)
            if orders_ser.is_valid():
                orders_ser.save()
            else:
                return Response(orders_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(main_order_ser.data, status=status.HTTP_200_OK)
    else:
        return Response(main_order_ser.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteOrders(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = models.MainOrder.objects.all()

    def get_queryset(self):
        id_list = models.OrderList.objects.filter(main_order=self.kwargs['pk']).values_list('order', flat=True)
        # print(id_list)
        order_product_queryset = models.OrderProduct.objects.filter(pk__in=id_list)
        product_id_list = order_product_queryset.values_list('product', flat=True)
        price_list = models.Product.objects.filter(pk__in=product_id_list).values_list('price', flat=True)
        price_sum = sum(price_list)
        orders_deleted = order_product_queryset.delete()
        main_order = models.MainOrder.objects.filter(pk=self.kwargs['pk'],
                                                     user=self.request.user)
        main_order_user_list = main_order.values_list('user', flat=True)
        # print(main_order_user_list[0])
        user_update = models.User.objects.get(pk=main_order_user_list[0])
        # print(user_update.credit - price_sum)
        if (user_update.credit - price_sum) > 0:
            user_update.credit = user_update.credit - price_sum
            user_update.save()
        else:
            raise ValidationError(detail="You don't have enough money")
        return main_order


class GetMainOrder(generics.RetrieveAPIView):
    queryset = models.MainOrder.objects.all()
    serializer_class = serializers.MainOrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        obj = models.MainOrder.objects.filter(user=request.user.pk)
        serializer = self.serializer_class(obj, many=True)
        return Response(serializer.data)


class DeleteOrder(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, ]  # + IsOwner
    queryset = models.OrderProduct.objects.all()

    def get_queryset(self):
        return models.OrderProduct.objects.filter(pk=self.kwargs['pk'], user=self.request.user)