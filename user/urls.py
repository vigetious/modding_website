from django.urls import path, include

from . import views

app_name = 'user'

urlpatterns = [
    path('user/', views.user, name='userPage')
]
