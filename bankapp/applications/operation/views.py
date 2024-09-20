from django.shortcuts import render
#
from rest_framework.response import Response
#
from rest_framework import status
#
from rest_framework.views import APIView
#
from .models import Operation
#
from .serializers import OperationSerializer
# Create your views here.

class AddOperationView(APIView):
    serializer_class = OperationSerializer
    
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        operation = Operation.objects.create(
            description=serializer.validated_data['description']
        )

        return Response(
            {   
                'status' : status.HTTP_201_CREATED,
                'message': 'Operacion creada exitosamente',
                'operation' : operation.description
            }
        )
    
