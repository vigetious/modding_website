from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from mod.models import Mod

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mod
        fields = ['modID']


class UserViewSet(viewsets.ModelViewSet):
    queryset = Mod.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    #path('api/', include(router.urls)),
    #path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]