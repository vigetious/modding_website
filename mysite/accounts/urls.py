from django.urls import path, include

from . import views

app_name = 'accounts'

urlpatterns = [
    path('account/', views.account, name='accountPage'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/edit/', views.edit, name='edit'),
    path('profile/avatar', views)
    path('accounts/', include('django.contrib.auth.urls')),
]
