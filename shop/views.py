from django.shortcuts import render
from rest_framework import generics, viewsets, status
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


class GetCategoryById(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get(self, request, pk, *args, **kwargs):
        category_id_list = models.SubCategory.objects.filter(category=pk).values_list('sub_category',
                                                                                      flat=True)
        obj = models.Category.objects.filter(pk__in=category_id_list)
        serializer = self.serializer_class(obj, many=True)
        return Response(serializer.data)


class CreateProduct(generics.CreateAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()

    def create(self, request, *args, **kwargs):
        context1 = {
            'name': request.data["post"],
            'color1': request.data["color1"],
            'color2': request.data["color2"],
            'color3': request.data["color3"],
            'price': request.data["price"],
            'seller': request.data["seller"],
            'picture': request.data["picture"]
        }
        self.context2 = {
            'category1': request.data["category1"],
        }
        self.context3 = {
            'category1': request.data["category1"],
        }

        serializer = self.get_serializer(data=context1)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        obj = serializer.save()
        self.context2['product'] = obj.id
        self.context3['product'] = obj.id
        cp_serializer1 = serializers.CategoryProductSerializer(data=self.context2)
        cp_serializer2 = serializers.CategoryProductSerializer(data=self.context3)
        if cp_serializer1.is_valid() and cp_serializer2.is_valid():
            cp_serializer1.save()
            cp_serializer2.save()
        else:
            return Response(cp_serializer1.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteProduct(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, ]    # + IsOwner
    queryset = models.Product.objects.all()

    def get_queryset(self):
        return models.Product.objects.filter(pk=self.kwargs['pk'], seller=self.request.user)
