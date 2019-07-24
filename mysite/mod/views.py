from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.views.generic.list import ListView
from django.db.models import F, Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from django_filters.views import FilterView
from taggit.models import Tag

from .forms import SubmitForm
from .models import Mod#, ModFilter
from .scripts import moveMod

# Create your views here.


def index(request):
    return render(request, 'mod/index.html')


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
            post.save()
            form.save_m2m()
            return redirect('mod:modPage', pk=post.pk)
    else:
        form = SubmitForm()

    return render(request, 'mod/submitMod.html', {'form': form})


def modPage(request, pk):
    post = get_object_or_404(Mod, pk=pk)
    post.tags = Tag.objects.all()
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


def modTagFilter(request):
    mods = Mod.objects.filter(tags__name__in=["depressing", "sad"]).distinct()
    tags = Tag.objects.all()

    return render(request, 'mod/modTagFilter.html', {'mods': mods, 'tags': tags})
# use query like search to add to use with search

#class PostList(FilterView):
#    model = Mod
#    context_object_name = 'posts'
#    filter_class = ModFilter

class SearchResultsView(ListView):
    model = Mod
    template_name = 'mod/modSearch.html'

    def get_queryset(self):
        searchQuery = self.request.GET.get('search')
        tagFilter = self.request.GET.get('tags')
        #tagFilter = "sad"
        if tagFilter is None and searchQuery is not None:
            object_list = Mod.objects.filter(
                Q(modName__contains=searchQuery) | Q(modDescription__contains=searchQuery)
            )
        elif searchQuery is None and tagFilter is not None:
            object_list = Mod.objects.filter(
                tags__name__in=[tagFilter]
            )
        elif searchQuery is not None and tagFilter is not None:
            object_list = Mod.objects.filter(
                Q(modName__contains=searchQuery) | Q(modDescription__contains=searchQuery), tags__name__in=[tagFilter]
            )
        else:
            return HttpResponse("Please enter something in the search parameter")
        return object_list

    def get_tags(self):
        tags = Tag.objects.all()
        return tags


# not working - try getting it work later
#class SearchResultsView(ListView):
#    model = Mod
#    template_name = 'mod/modSearch.html'

#    def get_queryset(self):
#        query = SearchQuery(self.request.GET.get('q'))
#        results = Mod.objects.annotate(rank=SearchRank(F('modSearch'), query))\
#            .filter(modSearch=query).order_by('-rank').values_list('modID', 'modName', 'rank')
#        return results
