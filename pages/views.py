from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.apps import apps

from mod.models import Mod
from accounts.models import User
from .models import AdminNews

import pdb


def home(request):
    newMods = Mod.objects.filter(modApproved=True).order_by('-modDate')[:12]
    ratedMods = Mod.objects.filter(modApproved=True).order_by('-modRating')[:12]
    # reviewedMods = Mod.objects.filter(modApproved=True).order_by('-modReviewCount')[:12]
    reviewedMods = sorted(Mod.objects.filter(modApproved=True), key=lambda t: t.modReviewCount)  # order by review count using sorted
    adminNews = AdminNews.objects.all().order_by('-adminNewsDate')
    return render(request, 'pages/home.html', {'newMods': newMods, 'ratedMods': ratedMods, 'reviewedMods': reviewedMods, 'adminNews': adminNews})


def supportHome(request):
    return render(request, 'pages/supportHome.html')


def submittingMods(request):
    return render(request, 'pages/submittingModsSupport.html')


def otherUsersMods(request):
    return render(request, 'pages/otherUsersModsSupport.html')


def myAccount(request):
    return render(request, 'pages/myAccountSupport.html')


def contactUs(request):
    return render(request, 'pages/contactUs.html')


def rules(request):
    return render(request, 'pages/rules.html')


def copyright(request):
    return render(request, 'pages/DMCA.html')

def privacypolicy(request):
    return render(request, 'pages/privacypolicy.html')

# Create your views here.
