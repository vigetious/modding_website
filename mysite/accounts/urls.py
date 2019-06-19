from django.urls import path, include

from . import views

app_name = 'accounts'

urlpatterns = [
    path('account/', views.account, name='accountPage'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]
