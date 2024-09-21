from rest_framework import serializers



class TransactionSerializer(serializers.Serializer):
    operation = serializers.IntegerField()
    destination_account = serializers.CharField(max_length=10)
    transaction_amount = serializers.IntegerField()