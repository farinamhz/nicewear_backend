from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('login/', views.CustomAuthToken.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    path('register/', views.UserRegistration.as_view()),
    path('create-address/', views.CreateAddress.as_view()),
    path('create-phone/', views.CreatePhone.as_view()),
    path('delete-address/<int:pk>/', views.DeleteAddress.as_view()),
    path('delete-phone/<int:pk>/', views.DeletePhone.as_view()),
    path('get-addresses/<int:pk>/', views.GetAddressById.as_view()),
    path('get-phones/<int:pk>/', views.GetPhoneById.as_view()),
]
