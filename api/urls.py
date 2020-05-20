from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from mod.models import Mod
from .views import latest, modSearch, modDownload


router = routers.DefaultRouter()

router.register(r'mod/modDownload', modDownload)
router.register(r'mod/latest', latest)
router.register(r'mod', modSearch)


urlpatterns = [
    path('', include(router.urls)),
    path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
