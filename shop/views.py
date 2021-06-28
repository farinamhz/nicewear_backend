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


