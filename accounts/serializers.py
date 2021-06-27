import re

from . import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'password', 'email', 'credit', 'role')
        extra_kwargs = {'password': {'write_only': True}, 'email': {'write_only': True}}
        # read_only_fields = 'credit'


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Phone
        fields = "__all__"

    def validate_phone(self, value):
        pattern = re.compile("^\+?[1-9]\d{1,14}$")
        if pattern.match(value) is None:
            raise serializers.ValidationError("the format of phone is invalid")
        return value


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = "__all__"
