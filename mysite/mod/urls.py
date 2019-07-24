from django.urls import path, include

from . import views

from .views import SearchResultsView

app_name = 'mod'

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit, name='submit'),
    path('<int:pk>/', views.modPage, name='modPage'),
    path('<int:pk>/edit', views.modEdit, name='modEdit'),
    path('<int:pk>/delete', views.modDelete, name='modDelete'),
    path('search/', SearchResultsView.as_view(), name='modSearch'),
    path('filter/', views.modTagFilter, name='modTagFilter'),
]
