from django.shortcuts import render

from rest_framework import viewsets, serializers
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter

from mod.models import Mod
from .serializers import ModSerializer

# Create your views here.


class latest(viewsets.ReadOnlyModelViewSet):
    queryset = Mod.objects.filter(modShow=True).order_by('-modDate')[:0]
    serializer_class = ModSerializer

    def get_queryset(self):
        latestMod = Mod.objects.filter(modShow=True).order_by('-modID')[0]
        return Mod.objects.filter(modID=latestMod.modID)


class modSearch(viewsets.ReadOnlyModelViewSet):
    queryset = Mod.objects.all()
    serializer_class = ModSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['modID', 'modAuthor', 'modDate', 'modUpdate', 'modStatus', 'modName', 'modRating', 'modNSFW']
