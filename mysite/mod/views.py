from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import SubmitForm
from .models import Mod
from .scripts import moveMod

# Create your views here.

#def index(request):
#    template = loader.get_template('mod/index.html')
#    return HttpResponse(template.render(request))

def index(request):
    return render(request, 'mod/index.html')

#def submit(request):
#    return render(request, 'mod/submitMod.html')


@login_required
def submit(request):
    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.modAuthor = request.user
            post.modDate = timezone.now()
            post.modUpdate = timezone.now()
            post.save()
            #post.modUploadURL = 'files/{0}/{1}'.format(str(post.modAuthor.id), post.modUpload.name)
            #post.modUpload.path = #moveMod(post.modID, post.modUpload.path, post.modName)
            post.save()
            form.save_m2m()
            return redirect('mod:modPage', pk=post.pk)
    else:
        form = SubmitForm()

    return render(request, 'mod/submitMod.html', {'form': form})


def modPage(request, pk):
    post = get_object_or_404(Mod, pk=pk)
    return render(request, 'mod/modPage.html', {'post': post})


def modEdit(request, pk):
    post = get_object_or_404(Mod, pk=pk)
    if request.method == 'POST':
        form = SubmitForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.modAuthor = request.user
            post.modUpdate = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('mod:modPage', pk=post.pk)
    else:
        form = SubmitForm(instance=post)
    return render(request, 'mod/modEdit.html', {'form': form, 'post': post})


def modDelete(request, pk):
    post = get_object_or_404(Mod, pk=pk)
    post.delete()
    return redirect('accounts:accountPage')
