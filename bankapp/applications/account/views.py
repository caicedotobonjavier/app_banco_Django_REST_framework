from django.shortcuts import render
#
from .serializers import AccountSerializer
#
from .models import Account, TypeAccount
#
from applications.users.models import User
#
from rest_framework.views import APIView
#
from rest_framework.permissions import IsAuthenticated
#
from rest_framework.authentication import TokenAuthentication
#
from rest_framework.response import Response
#
from rest_framework import status
#
from .functions import create_account
# Create your views here.


class AccountView(APIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = Account.objects.create(
            account_number = create_account(),
            user_id = User.objects.get(user_id=serializer.validated_data['user_id'])
        )

        type_account = TypeAccount.objects.create(
            account = account,
            account_type = serializer.validated_data['account_type']
        )

        return Response(
            {   
                'status' : status.HTTP_201_CREATED,
                'message' : 'Cuenta creada exitosamente',
                'user' : account.user_id.full_name,
                'account_number' : account.account_number,
                'account_type' : type_account.get_account_type_display()
            }
        )