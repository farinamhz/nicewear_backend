from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response

from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
# Create your views here.


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "id": user.pk,
            "username": user.username,
            "credit": user.credit,
            "role": user.role,
            'token': token.key,
        })


class LogoutAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    # def get(self, request):
    #     # simply delete the token to force a login
    #     request.user.auth_token.delete()
    #     return Response(status=status.HTTP_200_OK)
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserRegistration(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token, create = Token.objects.get_or_create(user=user)
                data_response = serializer.data
                data_response['token'] = token.key
                return Response(data_response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
