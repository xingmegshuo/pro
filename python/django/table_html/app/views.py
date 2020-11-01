from rest_framework import viewsets
from .serializer import computerSerializers,infoSerializers
from .models import  Computer,info

from django.shortcuts import render


class computerViewSet(viewsets.ModelViewSet):
    queryset = Computer.objects.all()
    serializer_class = computerSerializers


class infoViewSet(viewsets.ModelViewSet):
    queryset = info.objects.all()
    serializer_class = infoSerializers


def index(request):
    return render(request, 'index.html')