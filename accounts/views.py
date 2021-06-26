from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from rest_framework.views import APIView
# Create your views here.


class LogoutAPIView(APIView):
    pass


class UserRegistration(CreateAPIView):

    def get_serializer_class(self):
        self.serializer_class = UserSerializer
        return self.serializer_class
