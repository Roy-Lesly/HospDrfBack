from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from .serializers import (
        WardSerializer, 
    )
from .models import Ward


class WardView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = WardSerializer
    queryset = Ward.objects.all()