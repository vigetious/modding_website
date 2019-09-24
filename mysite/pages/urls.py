from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('support/', views.supportHome, name='supportHome'),
    path('support/submittingmods/', views.submittingMods, name='submittingMods'),
    path('support/otherusers/', views.otherUsersMods, name='otherUsersMods'),
    path('support/myaccount/', views.myAccount, name='myAccountSupport'),
    path('support/contactus/', views.contactUs, name='contactUs'),
    path('support/rules/', views.rules, name='rules'),
    path('support/copyright', views.copyright, name='copyright'),
    path('support/copyright', views.copyright, name='copyright'),
    path(r'^taggit/', include('taggit_selectize.urls')),
    path(r'^verified-email-field/', include('verified_email_field.urls')),
]


