from django.shortcuts import render
#
from .serializers import CardSerializer
#
from rest_framework.response import Response
#
from rest_framework.views import APIView
# Create your views here.



class AddCardView(APIView):
    serializer_class = CardSerializer

    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        
        return Response(
            {
                'message' : 'OK'
            }
        )
    




