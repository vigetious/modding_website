from django.urls import path, include

from . import views

from .views import SearchResultsView

app_name = 'mod'

urlpatterns = [
    path('submit/', views.submit, name='submit'),
    path('<int:pk>/', views.modPage, name='modPage'),
    path('<int:pk>/edit', views.modEdit, name='modEdit'),
    path('<int:pk>/delete', views.modDelete, name='modDelete'),
    path('search/', SearchResultsView.as_view(), name='modSearch'),
    path('filter/', views.modTagFilter, name='modTagFilter'),
    path('likes/', include('likes.urls')),
    path('<int:pk>/reviewupvote/', views.reviewUpVote, name='reviewUpvote'),
    path('<int:pk>/reviewremovevote/', views.reviewRemoveVote, name='reviewRemoveVote'),
    path('<int:pk>/reviewdownvote/', views.reviewDownVote, name='reviewDownvote'),
    path('<int:pk>/reviewdelete/', views.reviewDelete, name='reviewDelete'),
    path('<int:pk>/rating/', views.rating, name='rating'),
    path('<int:pk>/ratingdelete/', views.ratingDelete, name='ratingDelete'),
    path('<int:pk>/news/', views.news, name='news'),
    path('<int:pk>/notifications/', views.notification, name='notification'),
]
