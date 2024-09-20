from django.shortcuts import render
#
from applications.card.models import Card
#
from applications.users.models import User
#
from applications.account.models import Account, TypeAccount
#
from .serializers import CardSerializer
#
from rest_framework import status
#
from rest_framework.response import Response
#
from rest_framework.views import APIView
#
import datetime
# Create your views here.



class AddCardView(APIView):
    serializer_class = CardSerializer

    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(user_id=serializer.validated_data['user'])
        account = Account.objects.get(account_id=serializer.validated_data['account'])
        type_account = TypeAccount.objects.get(account = account.account_number)
        membership_date = datetime.datetime.now()
        expiration_date = serializer.validated_data['expiration_date']
        balance = serializer.validated_data['balance']

        cards = Card.objects.filter(account=account).exists()
        
        if cards:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Ya existe una tarjeta asociada a esta cuenta'
                }
            )
            
        else:
            card = Card.objects.create(
                user=user,
                account=account,
                type_account=type_account,
                membership_date=membership_date,
                expiration_date=expiration_date,
                balance=balance
            )
            return Response(
                {
                    'status' : status.HTTP_201_CREATED,
                    'message' : 'Tarjeta creada corretamente',
                    'nro_card' : card.card_id,
                    'user' : card.user.full_name,
                    'balance' : balance,
                    'membership_date' : membership_date,
                    'expiration_date' : expiration_date
                }
            )