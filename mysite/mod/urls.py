from django.urls import path, include

from . import views

app_name = 'mod'

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit, name='submit'),
    path('<int:pk>/', views.modPage, name='modPage'),
    path('<int:pk>/edit', views.modEdit, name='modEdit')
]
