from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm, edit#, SignUp


# Create your views here.

@login_required
def account(request):
    return render(request, 'accounts/accountPage.html')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
def edit(request):
    user = request.user

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            user.save()
            return redirect('accounts:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/edit.html", {'form': form})


def avatar(request):
    


#class SignUp(generic.CreateView):
#    form_class = SignUp
#    success_url = reverse_lazy('login')
#    template_name = 'registration/signup.html'
