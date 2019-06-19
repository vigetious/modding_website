from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from .forms import SubmitForm

# Create your views here.

#def index(request):
#    template = loader.get_template('mod/index.html')
#    return HttpResponse(template.render(request))

def index(request):
    return render(request, 'mod/index.html')

#def submit(request):
#    return render(request, 'mod/submitMod.html')

def get_submit(request):
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/submitted/')
    else:
        form = SubmitForm()

    return render(request, 'mod/submitMod.html', {'form': form})
