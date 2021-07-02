from rest_framework import status, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from . import permissions


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
    permission_classes = (IsAuthenticated,)

    # def get(self, request):
    #     # simply delete the token to force a login
    #     request.user.auth_token.delete()
    #     return Response(status=status.HTTP_200_OK)
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserRegistration(APIView):

    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token, create = Token.objects.get_or_create(user=user)
                data_response = serializer.data
                data_response['token'] = token.key
                return Response(data_response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateAddress(generics.CreateAPIView):
    serializer_class = serializers.AddressSerializer
    queryset = models.Address.objects.all()
    permission_classes = (IsAuthenticated, permissions.IsUser)


class CreatePhone(generics.CreateAPIView):
    serializer_class = serializers.PhoneSerializer
    queryset = models.Phone.objects.all()
    permission_classes = (IsAuthenticated, permissions.IsUser)


class DeleteAddress(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.IsOwnerToDeleteAddress]  # + IsOwner
    queryset = models.Address.objects.all()

    def get_queryset(self):
        return models.Address.objects.filter(pk=self.kwargs['pk'], user=self.request.user)


class DeletePhone(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, permissions.IsOwnerToDeletePhone]  # + IsOwner
    queryset = models.Phone.objects.all()

    def get_queryset(self):
        return models.Phone.objects.filter(pk=self.kwargs['pk'], user=self.request.user)


class GetAddressById(generics.RetrieveAPIView):
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer
    permission_classes = [IsAuthenticated, permissions.IsOwner]

    def get(self, request, *args, **kwargs):
        obj = models.Address.objects.filter(user__pk=self.kwargs['pk'])
        serializer = self.serializer_class(obj, many=True)
        return Response(serializer.data)


class GetPhoneById(generics.RetrieveAPIView):
    queryset = models.Phone.objects.all()
    serializer_class = serializers.PhoneSerializer
    permission_classes = [IsAuthenticated, permissions.IsOwner]

    def get(self, request, *args, **kwargs):
        obj = models.Phone.objects.filter(user__pk=self.kwargs['pk'])
        serializer = self.serializer_class(obj, many=True)
        return Response(serializer.data)
