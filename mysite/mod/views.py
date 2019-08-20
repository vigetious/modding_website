from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.db.models import F, Q, Count, Sum, Avg
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

import json, pdb

from django_filters.views import FilterView
from taggit.models import Tag

from .forms import SubmitForm, ReviewForm, VoteForm
from .models import Mod, ReviewRating, Vote, Rating#, ModFilter
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
    review = ReviewRating.objects.filter(reviewModID=post.modID)
    vote = Vote.objects.all()  # you dont need to get all; only one value so use mod id to get field
    # use reviewrating.reviewModID if you have to
    if request.user.is_authenticated:
        try:
            rating = Rating.objects.get(ratingAuthorID=request.user)
        except ObjectDoesNotExist:
            rating = None
    else:
        rating = None
    #rating = Rating.objects.get(ratingAuthorID=request.user)
    questions = ReviewRating.objects.annotate(number_of_votes=Sum('vote'))
    #yaes = ReviewRating.objects.annotate(x=Count('vote')).annotate(number_of_votes=Sum('x'))
#    for c in ReviewRating.objects.all():
#        #x = Vote.objects.filter(voteReviewID=review.reviewid)
#        for x in Vote.objects.filter(voteReviewID=c.reviewid):
#            t = ReviewRating.objects.get(reviewid=c.reviewid)
#            t.reviewVotes = x.objects.annotate()
    #review = ReviewRating.objects.all()
    post.tags = Tag.objects.all()
    #pdb.set_trace()
    if request.method == 'POST':
        commentForm = ReviewForm(request.POST)
        if commentForm.is_valid():
            postReview = commentForm.save(commit=False)
            postReview.reviewModID = Mod.objects.get(modID=post.modID)
            postReview.reviewAuthor = request.user
            postReview.save()
            return redirect('mod:modPage', pk=post.pk)
    else:
        commentForm = ReviewForm()
    return render(request, 'mod/modPage.html', {'post': post, 'commentForm': commentForm, 'review': review,
                                                'vote': vote, 'questions': questions, 'rating': rating})


@login_required
def reviewUpVote(request, pk):
    if request.method == 'POST':
        request_getdata = request.POST.get('id')
        voteReviewID = ReviewRating.objects.get(reviewid__exact=request_getdata)
        response_data = {}
        post = Vote(voteReviewID=voteReviewID, voteAuthor=request.user, voteValue=1)
        post.save()
        reviewrating = ReviewRating.objects.get(reviewid=voteReviewID)
        allVotes = Vote.objects.filter(voteReviewID__exact=request_getdata).count()
        reviewrating.reviewVotes = allVotes
        reviewrating.save()
        response_data['result'] = "Successfully upvoted review " + request_getdata

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
def reviewRemoveVote(request, pk):
    if request.method == 'POST':
        response_data = {}
        request_getdata = request.POST.get('id')
        voteReviewID = ReviewRating.objects.get(reviewid__exact=request_getdata)
        reviewrating = ReviewRating.objects.get(reviewid=voteReviewID)
        Vote.objects.get(voteReviewID__exact=voteReviewID, voteAuthor=request.user).delete()
        allVotes = Vote.objects.filter(voteReviewID__exact=request_getdata).count()
        reviewrating.reviewVotes = allVotes
        reviewrating.save()
        response_data['result'] = "Successfully removed vote from review " + request_getdata

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
def reviewDownVote(request, pk):
    if request.method == 'POST':
        request_getdata = request.POST.get('id')
        voteReviewID = ReviewRating.objects.get(reviewid__exact=request_getdata)
        response_data = {}
        post = Vote(voteReviewID=voteReviewID, voteAuthor=request.user, voteValue=-1)
        post.save()
        reviewrating = ReviewRating.objects.get(reviewid=voteReviewID)
        votesAgg = Vote.objects.filter(voteReviewID__exact=request_getdata).aggregate(totalVoted=Sum('voteValue'))['totalVoted']
        #allVotes = Vote.objects.aggregate(totalVoted=Sum(votesAgg))
        reviewrating.reviewVotes = votesAgg
        reviewrating.save()
        response_data['result'] = "Successfully downvoted review " + request_getdata

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
def reviewDelete(request, pk):
    if request.method == 'POST':
        request_getdata = request.POST.get('id')
        ReviewRating.objects.get(reviewid__exact=request_getdata).delete()
        response_data = {}
        response_data['result'] = "Successfully deleted review " + request_getdata

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def rating(request, pk):
    if request.method == "POST":
        request_modID = request.POST.get('modID')
        request_value = request.POST.get('value')

        modID = Mod.objects.get(modID__exact=request_modID)
        response_data = {}
        post = Rating(ratingModID=modID, ratingAuthorID=request.user, ratingValue=request_value)
        post.save()

        averageRating = Rating.objects.filter(ratingModID=request_modID).aggregate(Avg(('ratingValue')))['ratingValue__avg']  # getting average rating for the mod we are using
        modID.modRating = averageRating
        modID.save()  # updating mod average rating

        response_data['result'] = "Successfully rated mod {0} with a {1}/5.".format(request_modID, request_value)
        response_data['data'] = serializers.serialize('json', Rating.objects.filter(ratingID=post.ratingID))

        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type='application/json'
        )


def ratingDelete(request, pk):
    if request.method == 'POST':
        ratingID = request.POST.get('ratingID')

        Rating.objects.get(ratingID=ratingID).delete()
        response_data = {}
        response_data['result'] = "Successfully delete rating " + ratingID

        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type='application/json'
        )


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

