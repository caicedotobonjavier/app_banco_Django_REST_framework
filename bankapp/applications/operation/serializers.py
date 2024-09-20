from rest_framework import serializers


class OperationSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=50, required=True)