from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

# path('get-relation-categories/', GetSubCategories.as_view()),

urlpatterns = [
    path('create-category/', views.CreateCategory.as_view()),
    path('create-subcategory/', views.CreateSubCategory.as_view()),
    path('get-categories/', views.GetCategories.as_view()),
    path('get-categories/<int:pk>/', views.GetCategoryById.as_view()),
    path('create-product/', views.CreateProduct.as_view()),
    path('delete-product/<int:pk>/', views.DeleteProduct.as_view()),
    path('get-product/<int:pk>/', views.get_product),
    path('get-product-category1/<int:pk>/', views.GetProductByCategory1.as_view()),
    path('get-product-category1-category2/<int:pk1>/<int:pk2>/', views.GetProductByCategories.as_view()),
    path('create-comment/<int:pk1>', views.CreateCategory.as_view()),
]
