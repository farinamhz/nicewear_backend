from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('create-category/', views.CreateCategory.as_view()),
    path('create-subcategory/', views.CreateSubCategory.as_view()),
    path('get-categories/', views.GetCategories.as_view()),
    # path('get-relation-categories/', GetSubCategories.as_view()),
    path('get-categories/<int:pk>/', views.GetCategoryById.as_view()),
    path('delete-product/<int:pk>/', views.DeleteProduct.as_view()),
]
