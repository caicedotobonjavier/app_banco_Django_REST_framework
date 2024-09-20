from rest_framework import serializers
#
from .models import User
#
from django.contrib.auth.hashers import check_password


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(max_length=150, required=True)
    date_birth = serializers.DateField(required=False)
    phone = serializers.CharField(max_length=15, required=False)
    address = serializers.CharField(max_length=50, required=False)
    password = serializers.CharField(max_length=128, required=True)



class ActivateUserSeralizer(serializers.Serializer):
    code = serializers.CharField(max_length=6, required=True)

    def validate(self, data):
        user = self.context.get('pk')
        code = data['code']
        usuario = User.objects.get(user_id=user)

        print(code)
        print(usuario)
        print(usuario.activation_code)
        

        if usuario.activation_code != code:
            raise serializers.ValidationError("El codigo de activacion no es valido")
        
        return data


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)



class VerifyLoginSerializer(serializers.Serializer):
    code_verify = serializers.CharField(max_length=6 ,required=True)

    def validate(self, data):
        id = self.context.get('pk')
        code = data['code_verify']
        
        user = User.objects.get(user_id=id)

        if check_password(code, user.login_otp) and user.user_login_otp==True:
            raise serializers.ValidationError("Este codigo esta vencido, debe iniciar sesion de nuevo para obtener nuevo codigo")
        
        if not check_password(code, user.login_otp):
            raise serializers.ValidationError("El codigo de verificacion no es valido")

        return data



class UpdateUserSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    date_birth = serializers.DateField(required=False, allow_null=True)
    phone = serializers.CharField(max_length=15,required=False, allow_blank=True)
    address = serializers.CharField(max_length=50, required=False, allow_blank=True)
    password = serializers.CharField(max_length=128, required=False, allow_blank=True)