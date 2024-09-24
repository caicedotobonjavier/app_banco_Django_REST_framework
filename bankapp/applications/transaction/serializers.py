from rest_framework import serializers




# La clase `TransactionSerializer` define un serializador para datos de transacciones con campos para
# operación, cuenta de destino y monto de la transacción.
class TransactionSerializer(serializers.Serializer):
    operation = serializers.IntegerField()
    destination_account = serializers.CharField(max_length=10)
    transaction_amount = serializers.IntegerField()




# La clase `DepositWithdrawAccountSerializer` es un serializador en Python para manejar operaciones de depósito y
# retiro con montos de transacción.
class DepositWithdrawAccountSerializer(serializers.Serializer):
    operation = serializers.IntegerField()
    transaction_amount = serializers.IntegerField()