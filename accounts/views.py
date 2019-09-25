from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.views import generic
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
#from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import PasswordResetView

from .forms import CustomUserCreationForm, EditForm, AvatarForm#, SignUp
from .models import Avatar, User

from mod.models import Mod
from mod.models import Rating
from mod.models import ReviewRating

import json, pdb


# Create your views here.


@login_required
def profile(request):
    try:
        userAvatar = Avatar.objects.get(avatarUserID=request.user)
    except ObjectDoesNotExist:
        #userAvatar = None
        userAvatar = Avatar.objects.create(avatarUserID=request.user, avatarImage='files/avatar/icon.png')

    try:
        mods = Mod.objects.filter(modAuthor=request.user.id)
    except:
        mods = "No mods found!"

    played = Rating.objects.filter(ratingAuthorID=request.user.id)
    reviews = ReviewRating.objects.filter(reviewAuthorID=request.user.id)

    return render(request, 'accounts/profile.html', {'avatar': userAvatar, 'mods': mods, 'played': played,
                                                     'reviews': reviews})


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class PasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('login')
    template_name = 'registration/password_reset_form.html'


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/changePassword.html', {
        'form': form
    })

def userProfile(request, pk):
    post = get_object_or_404(User, pk=User.objects.get(username=pk).id)
    #avatar = Avatar.objects.get(avatarUserID=pk)
    try:
        userAvatar = Avatar.objects.get(avatarUserID=User.objects.get(username=pk).id)
    except ObjectDoesNotExist:
        userAvatar = None
    try:
        mods = Mod.objects.filter(modAuthor=User.objects.get(username=pk).id)
    except ObjectDoesNotExist:
        mods = "No mods found!"

    played = Rating.objects.filter(ratingAuthorID=User.objects.get(username=pk).id)
    reviews = ReviewRating.objects.filter(reviewAuthorID=User.objects.get(username=pk).id)
    return render(request, 'accounts/userProfile.html', {'post': post, 'avatar': userAvatar, 'mods': mods,
                                                         'played': played, 'reviews': reviews})


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


@login_required
def avatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.avatarUserID = request.user
            try:
                if Avatar.objects.get(avatarUserID=request.user):
                    Avatar.objects.get(avatarUserID=request.user).delete()
            except:
                pass
            if post.avatarImage:
                pass
            else:
                post.avatarImage = 'files/avatar/icon.png'
            post.save()
            return redirect('accounts:profile')
    else:
        form = AvatarForm()
    return render(request, 'accounts/avatar.html', {'form': form})


@login_required
def bio(request):
    if request.method == 'POST':
        newBio = request.POST.get('message')
        user = User.objects.get(id=request.user.id)
        user.description = newBio
        user.save()
        response_data = {}
        response_data['result'] = 'Successfully updated description.'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required
def note(request):
    if request.method == 'POST':
        newNote = request.POST.get('note')
        ratingID = request.POST.get('ratingID')
        rating = Rating.objects.get(ratingID=ratingID)
        rating.ratingNote = newNote
        rating.save()
        response_data = {}
        response_data['result'] = 'Successfully updated note.'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )



#class SignUp(generic.CreateView):
#    form_class = SignUp
#    success_url = reverse_lazy('login')
#    template_name = 'registration/signup.html'
