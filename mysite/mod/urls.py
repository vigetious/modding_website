from django.urls import path, include

from . import views

app_name = 'mod'

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.get_submit, name='submit'),
]
