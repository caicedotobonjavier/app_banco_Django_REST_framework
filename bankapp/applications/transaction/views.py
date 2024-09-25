from django.shortcuts import render
#
from .serializers import TransactionSerializer, DepositWithdrawAccountSerializer
#
from applications.users.models import User
#
from applications.operation.models import Operation
#
from applications.transaction.models import Transaction
#
from applications.account.models import Account, TypeAccount
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



# Esta clase de Python define una vista para procesar transacciones, incluida la validación y ejecución de
# la transacción en función de la entrada del usuario y los saldos de la cuenta.
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


# Esta clase de Python define una vista para buscar y mostrar información de saldo relacionada con la
#cuenta y los detalles de la tarjeta de un usuario.
class SearchBalanceView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        usuario = self.request.user
        user = User.objects.get(email=usuario)
        cuenta = Account.objects.get(user_id=usuario.user_id)
        tarjeta = Card.objects.get(user=usuario)
        tipo_cuenta = TypeAccount.objects.get(account=cuenta)
        
        return Response(
            {
                'status' : status.HTTP_200_OK,
                'user' : usuario.full_name,
                'account_number' : cuenta.account_number,
                'type_account' : str(tipo_cuenta),
                'balance' : tarjeta.balance
            }
        )



# Esta clase de Python define una vista API que recupera y formatea datos de transacciones para un
# usuario específico.
class OperationsUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        id = self.request.user
        transactions = Transaction.objects.filter(
            user=id
        )
        numero = 1
        operaciones = {}
        for t in transactions:
            operacion = {}
            operacion['date'] = t.transaction_date.date()
            operacion['operation'] = str(t.operation)
            operacion['destination_account'] = t.destination_account
            operacion['amount'] = t.transaction_amount
            operaciones[numero] = operacion
            numero += 1
        print(operaciones)



        return Response(
            {
                'status' : status.HTTP_200_OK,
                'operation' : operaciones
            }
        )


# Esta clase de Python define una vista API para recuperar transacciones por fecha para un usuario específico.
class TransactionByDate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = self.request.user

        fecha1 = self.request.query_params.get('date1', None),
        fecha2 = self.request.query_params.get('date2', None)
        fecha_1 = ''.join(fecha1)
        fecha_2 = ''.join(fecha2)
        
        transaction = Transaction.objects.transaction_date(
            user=user,
            date1 = fecha_1,
            date2 = fecha_2
        )
        
        operaciones={}
        number = 1
        for t in transaction:                   
            operacion={}
            operacion['tipo_operacion'] = t.operation.description
            operacion['fecha_operacion'] = t.transaction_date.date()
            operacion['cuenta_destino'] = t.destination_account
            operacion['monto'] = t.transaction_amount
            operaciones[number]=operacion
            number+=1

        if operaciones:
            return Response(
                {
                    'status' : status.HTTP_200_OK,
                    'message' : f'Las transacciones del usuario {user.full_name} entre [{fecha_1} y {fecha_2}]',
                    'data' : operaciones
                }
            )
        else:
            return Response(
                {
                    'status' : status.HTTP_200_OK,
                    'message' : 'No se encontraron transacciones en estas fechas'
                }
            )



# Esta clase define una vista para depositar y retirar fondos de la cuenta de un usuario usando una API REST
# en Django, manejando las transacciones en consecuencia.
class DepositWithdrawAccountView(APIView):
    serializer_class = DepositWithdrawAccountSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        account_user = Account.objects.get(user_id=user)
        card_user = Card.objects.get(user=user)
        operation = Operation.objects.get(id=serializer.validated_data['operation'])

        balance_account = card_user.balance

        print(operation.id)
        print(balance_account)


        if operation.id == 1:
            transaction = Transaction.objects.create(
                card = card_user,
                account = account_user,
                user = user,
                operation = operation,
                transaction_date = datetime.datetime.now(),
                destination_account = account_user,
                transaction_amount = serializer.validated_data['transaction_amount']
            )
            
            transaction.card.balance += serializer.validated_data['transaction_amount']
            transaction.card.save()

            return Response(
            {
                'status' : status.HTTP_202_ACCEPTED,
                'type_operation' : f'{transaction.operation}',
                'current_balance' : balance_account,
                'amount' : transaction.transaction_amount,
                'account' : transaction.account.account_number,
                'balance' : transaction.card.balance
            }
        )


        elif operation.id == 2 and card_user.balance >= serializer.validated_data['transaction_amount']:
            transaction = Transaction.objects.create(
                card = card_user,
                account = account_user,
                user = user,
                operation = operation,
                transaction_date = datetime.datetime.now(),
                destination_account = account_user,
                transaction_amount = serializer.validated_data['transaction_amount']
            )
            
            transaction.card.balance -= serializer.validated_data['transaction_amount']
            transaction.card.save()

            return Response(
            {
                'status' : status.HTTP_202_ACCEPTED,
                'type_operation' : f'{transaction.operation}',
                'current_balance' : balance_account,
                'amount' : transaction.transaction_amount,
                'account' : transaction.account.account_number,
                'balance' : transaction.card.balance
            }
        )

        else:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'No se pudo realizar la operacion, no tiene fondos suficientes'
                }
            )



# Esta clase Python define una vista para procesar pagos virtuales utilizando el marco REST de Django.
class VirtualPayView(APIView):
    serializer_class = TransactionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        card = Card.objects.get(user=user)
        account = Account.objects.get(user_id=user)
        operation = Operation.objects.get(id=serializer.validated_data['operation'])
        
        transaction = Transaction.objects.create(
            card = card,
            account = account,
            user = user,
            operation = operation,
            transaction_date = datetime.datetime.now(),
            destination_account = serializer.validated_data['destination_account'],
            transaction_amount = serializer.validated_data['transaction_amount']
        )

        account_desstiantion = Account.objects.get(account_number=transaction.destination_account)
        card_destination = Card.objects.get(account=account_desstiantion)
        card_destination.balance += transaction.transaction_amount
        card_destination.save()


        transaction.card.balance -= transaction.transaction_amount
        transaction.card.save()


        return Response(
            {
                'status' : status.HTTP_200_OK,
                'message' : 'Pago virtual realizado',
                'account' : transaction.destination_account,
                'amount' : transaction.transaction_amount
            }
        )



class DetailTransactionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        user = self.request.user

        details = Transaction.objects.details_transactions(user)
        actual_balance = Card.objects.get(user=user).balance

        return Response(
            {
                'status' : status.HTTP_200_OK,
                'actual_balance' : actual_balance,
                'message' : 'Details sum one by one transaction',
                'sum_all_transferencias' : details['sum_transferencias'],
                'sum_all_retiros' : details['sum_retiros'],
                'sum_all_consignaciones' : details['sum_consignaciones'],
                'sum_all_pagos_virtual' : details['sum_pagosvirtuales']
            }
        )