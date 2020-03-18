from django.urls import path, include

from . import views

from .views import SearchResultsView

app_name = 'mod'

urlpatterns = [
    path('submit/', views.submit, name='submit'),
    path('botlatest/', views.latest, name='latest'),
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
    path('<int:pk>/reviewedit/', views.reviewEdit, name='reviewEdit'),
    path('<int:pk>/rating/', views.rating, name='rating'),
    path('<int:pk>/ratingdelete/', views.ratingDelete, name='ratingDelete'),
    path('<int:pk>/news/', views.news, name='news'),
    path('<int:pk>/notifications/', views.notification, name='notification'),
    path('awards2018/', views.awards2018, name='awards2018'),
    path('awards2019/', views.awards2019, name='awards2019'),
]
