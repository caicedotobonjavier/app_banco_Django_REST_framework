from django.shortcuts import render
#
from django.shortcuts import get_object_or_404
#
from .models import User
#
from rest_framework.authtoken.models import Token
#
from .serializers import UserSerializer, LoginUserSerializer, UpdateUserSerializer
#
from rest_framework.views import APIView
#
from rest_framework.response import Response
#
from rest_framework.authentication import TokenAuthentication
#
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
#
from rest_framework import status
#
from .functions import create_cod
#
from django.contrib.auth import authenticate
# Create your views here.



# La clase `AddUserView` define un método POST para crear un nuevo usuario con campos específicos si el usuario
# aún no existe en la base de datos.
class AddUserVIew(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        full_name = serializer.validated_data['full_name']
        password = serializer.validated_data['password']
        phone= serializer.validated_data['phone']
        address = serializer.validated_data['address']
        date_birth = serializer.validated_data['date_birth']

        try:
            user_exists = get_object_or_404(User, email=email)
        except:
            user_exists = False


        if user_exists:
            return Response(
                {
                    'status' : status.HTTP_404_NOT_FOUND,
                    'error' : 'El usaurio que intenta registrar ya existe en la base de datos'
                }
            )
        else:
            user = User.objects.create_user(
                email,
                full_name,
                password,
                date_birth = date_birth,
                phone = phone,
                address = address                
            )

            user = {
                "email" : user.email,
                "full_name" : user.full_name,
                "date_birth" : user.date_birth,
                "phone" : user.phone,
                "address" : user.address
            }

            return Response(
                {
                    'status' : status.HTTP_201_CREATED,
                    'usuario_registrado' : user
                }
            )



# La clase `LoginUserView` maneja la autenticación del usuario validando las credenciales de inicio de sesión y generando
# un token para el usuario autenticado.
class LoginUserView(APIView):
    serializer_class = LoginUserSerializer    

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(email=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            
            user = {
                "email" : user.email,
                "full_name" : user.full_name,
                "token" : token.key
            }

            return Response(
                {
                    "status" : status.HTTP_200_OK,
                    "usuario_logueado" : user
                }
            )
        
        else:
            return Response(
                {
                    "status" : status.HTTP_404_NOT_FOUND,
                    "error" : "Usuario o contraseña incorrectos"
                }
            ) 



# La clase `UpdateUserView` es una vista API en Python que maneja la actualización de la información del usuario en función
# de los datos proporcionados en la solicitud.
class UpdateUserView(APIView):
    serializer_class = UpdateUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        #ver todo lo que trae el user request
        print(request.user.__dict__)
        #ver todo lo que trae el request
        print('*********************************************')
        print(request.__dict__)
        print('*********************************************')
        print(request.auth.__dict__)
        print('*********************************************')
        print(request.user.auth_token)
        print('*********************************************')
        print(request.user.auth_token.__dict__)
        
        if 'full_name' in serializer.data:
            user.full_name = serializer.validated_data['full_name']
        if 'phone' in serializer.data:
            user.phone = serializer.validated_data['phone']
        if 'address' in serializer.data:
            user.address = serializer.validated_data['address']
        if serializer.data['date_birth'] != None:
            user.date_birth = serializer.validated_data['date_birth']
        if 'password' in serializer.data:
            user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(
            {
                "status" : status.HTTP_200_OK,
                "message" : f"Se actualizo correctamente la informacion del usuario {user}"
            }
        )


# La clase `LogoutUserView` define una vista en una API del marco REST de Django para cerrar la sesión de un usuario
# eliminando su token de autenticación.
class LogoutUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        request.user.auth_token.delete()

        print(request.auth.__dict__)
        print('*********************************************')
        print(request.auth.key)


        return Response(
            {
                "status" : status.HTTP_200_OK,
                "message" : f"Se ha cerrado la sesion correctamente del usuario {user}"
            }
        )