from rest_framework import serializers
#


class CardSerializer(serializers.Serializer):    
    user = serializers.CharField(required=True)
    account = serializers.UUIDField(required=True)
    type_account = serializers.CharField(required=True)
    membership_date = serializers.DateField(required=True)
    expiration_date = serializers.DateField(required=True)
    balance = serializers.IntegerField(required=True)