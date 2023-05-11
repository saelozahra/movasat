from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

from .models import *
from rest_framework.views import APIView

# Create your views here.


class AghlamAPI(APIView):
    def get(self, request):
        try:
            aghlam = AghlamKomaki.objects.all()
            data = []
            for ghalam in aghlam:
                data.append(
                    {
                        "id": ghalam.id,
                        "name": ghalam.name,
                    }
                )
            return Response({"data": data}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
