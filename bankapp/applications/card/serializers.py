from rest_framework import serializers
#


class CardSerializer(serializers.Serializer):    
    user = serializers.CharField(required=True)
    account = serializers.UUIDField(required=True)
    expiration_date = serializers.DateField(required=True)
    balance = serializers.IntegerField(required=True)