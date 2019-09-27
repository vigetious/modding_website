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
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import AccountActivationTokenGenerator, account_activation_token
from django.contrib.auth import login

from .forms import CustomUserCreationForm, EditForm, AvatarForm#, SignUp
from .models import Avatar, User

from mod.models import Mod
from mod.models import Rating
from mod.models import ReviewRating

import json, pdb


# Create your views here.


def visitor_ip_address(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
def profile(request):
    try:
        userAvatar = Avatar.objects.get(avatarUserID=request.user)
    except ObjectDoesNotExist:
        #userAvatar = None
        userAvatar = Avatar.objects.create(avatarUserID=request.user, avatarImage=static('img/icon.png'))

    try:
        mods = Mod.objects.filter(modAuthor=request.user.id)
    except:
        mods = "No mods found!"

    played = Rating.objects.filter(ratingAuthorID=request.user.id)
    reviews = ReviewRating.objects.filter(reviewAuthorID=request.user.id)

    return render(request, 'accounts/profile.html', {'avatar': userAvatar, 'mods': mods, 'played': played,
                                                     'reviews': reviews})


#class SignUpView(CreateView):
#    form_class = CustomUserCreationForm
#    success_url = reverse_lazy('login')
#    template_name = 'registration/signup.html'

def SignUpView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Active your dokidokimodclub.com account"
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message, from_email='do-not-reply@dokidokimodclub.com')
            user.emai
            return redirect('accounts:account_activation_sent')
    else:
        form = CustomUserCreationForm
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'registration/account_activation_invalid.html')

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
            post.avatarIP = visitor_ip_address(request)
            try:
                if Avatar.objects.get(avatarUserID=request.user):
                    Avatar.objects.get(avatarUserID=request.user).delete()
            except:
                pass
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

def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')
