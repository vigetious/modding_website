from django.urls import path, include

from . import views
from mod.views import ratingDelete

app_name = 'accounts'

urlpatterns = [
    path('account/', views.account, name='accountPage'),
    path('profile/', views.profile, name='profile'),
    path('<int:pk>/profile', views.userProfile, name='userProfile'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/edit/', views.edit, name='edit'),
    path('profile/avatar', views.avatar, name='avatar'),
    path('profile/bio', views.bio, name='bio'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/played/', views.played, name='played'),
    path('<int:pk>/profile/played/', views.userPlayed, name='userPlayed'),
    path('played/ratingdelete/', ratingDelete, name='ratingDelete')
]
