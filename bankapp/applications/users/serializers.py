from rest_framework import serializers
#
from .models import User


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(max_length=150, required=True)
    date_birth = serializers.DateField(required=False)
    phone = serializers.CharField(max_length=15, required=False)
    address = serializers.CharField(max_length=50, required=False)
    password = serializers.CharField(max_length=128, required=True)



class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UpdateUserSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    date_birth = serializers.DateField(required=False, allow_null=True)
    phone = serializers.CharField(max_length=15,required=False, allow_blank=True)
    address = serializers.CharField(max_length=50, required=False, allow_blank=True)
    password = serializers.CharField(max_length=128, required=False, allow_blank=True)