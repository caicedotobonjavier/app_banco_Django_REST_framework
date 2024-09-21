from django.shortcuts import render
#
from .serializers import TransactionSerializer
#
from applications.users.models import User
#
from applications.operation.models import Operation
#
from applications.transaction.models import Transaction
#
from applications.account.models import Account
#
from applications.card.models import Card 
#
from rest_framework import status
#
from rest_framework.response import Response
#
from rest_framework.views import APIView
#
import datetime
#
from rest_framework.authentication import TokenAuthentication
#
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class TransactionView(APIView):
    serializer_class = TransactionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        card = Card.objects.get(user=user)
        acount = Account.objects.get(user_id=user)

        operation = Operation.objects.get(id=serializer.validated_data['operation'])
        destination_account = Account.objects.get(account_number=serializer.validated_data['destination_account'])
        amount = serializer.validated_data['transaction_amount']

        print(destination_account)
        print(card)
        print(acount)
        print(card.balance>= serializer.validated_data['transaction_amount'])

        if card and acount and (card.balance >= serializer.validated_data['transaction_amount']) and destination_account:
            operacion = Transaction.objects.create(
                card = card,
                account = acount,
                user = user,
                operation = operation,
                transaction_date = datetime.datetime.now(),
                destination_account = destination_account,
                transaction_amount = amount
            )

            card.balance -= int(amount)
            card.save()

            card_destino = Card.objects.get(account=destination_account)
            card_destino.balance += int(amount)
            card_destino.save()

            
            return Response(
                {   
                    'status' : status.HTTP_200_OK,
                    'operation' : operation.description,
                    'message' : f'Se realizo la {operation.description} de ${amount} en la cuenta {destination_account}',
                    'account_name' : f'{destination_account.user_id.full_name}'
                }
            )
        else:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'No se pudo realizar la operacion'
                }
            )
    