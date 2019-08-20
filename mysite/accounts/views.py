from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .forms import SignUp


# Create your views here.

@login_required
def account(request):
    return render(request, 'accounts/accountPage.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


class SignUp(generic.CreateView):
    form_class = SignUp
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
