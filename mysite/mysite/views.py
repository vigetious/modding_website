import sys
sys.path.append("..")

from django.shortcuts import render
from django.apps import apps
from mod.models import Mod
from accounts.models import User


def home(request):
    newMods = Mod.objects.all()
    if newMods is not None:
        yaes = "haha yup"
    else:
        yaes = "haha nop"
    return render(request, 'mysite/home.html', {newMods: "newMods", yaes: "yaes"})
