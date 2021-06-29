from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from . import serializers
from rest_framework.response import Response
from . import models


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


class GetProductByCategory2(generics.RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def get(self, request, *args, **kwargs):
        obj = models.Product.objects.filter(category2__pk=self.kwargs['pk'])
        serializer = self.serializer_class(obj, many=True)
        return Response(serializer.data)

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
