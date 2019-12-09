from django.urls import path, include

from . import views
from mod.views import ratingDelete

app_name = 'accounts'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('<str:pk>/profile', views.userProfile, name='userProfile'),
    path('signup/', views.SignUpView, name='signup'),
    path('account_activation_sent', views.account_activation_sent, name='account_activation_sent'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         views.activate, name='activate'),
    path('passwordReset/', views.PasswordResetForm, name='passwordReset'),
    path('passwordChange/', views.change_password, name='change_password'),
    path('profile/edit/', views.edit, name='edit'),
    path('profile/avatar', views.avatar, name='avatar'),
    path('profile/bio', views.bio, name='bio'),
    path('profile/note', views.note, name='note'),
    path('played/ratingdelete/', ratingDelete, name='ratingDelete'),
]
