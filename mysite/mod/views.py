from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.db.models import F, Q, Count, Sum, Avg
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core import serializers, mail
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

import json, pdb, math

from django_filters.views import FilterView
from taggit.models import Tag

from .forms import SubmitForm, ReviewForm, VoteForm, NewsForm
from .models import Mod, ReviewRating, Vote, Rating, News, NewsNotifications #, ModFilter
from .scripts import moveMod
from .operations.mail import notificationsSendMail

from accounts.models import User

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
            post.tags.add("All")
            user = User.objects.get(id=request.user.id)
            user.totalMods = user.totalMods + 1
            group = Group.objects.get(name="Mod Creators")
            group.user_set.add(request.user)
            user.save()
            return redirect('mod:modPage', pk=post.pk)
    else:
        form = SubmitForm()

    return render(request, 'mod/submitMod.html', {'form': form})


def modPage(request, pk):
    post = get_object_or_404(Mod, pk=pk)
    review = ReviewRating.objects.filter(reviewModID=post.modID)
    vote = Vote.objects.all()
    if request.user.is_authenticated:
        try:
            rating = Rating.objects.get(ratingAuthorID=request.user)
        except ObjectDoesNotExist:
            rating = None
    else:
        rating = None

    questions = ReviewRating.objects.annotate(number_of_votes=Sum('vote'))

    post.tags = Tag.objects.all()

    news = News.objects.filter(newsModID=pk)

    if request.user.is_authenticated:
        try:
            newsnotifications = NewsNotifications.objects.get(newsNotificationsModID=pk)
        except ObjectDoesNotExist:
            newsnotifications = None
    else:
        newsnotifications = None

    emails = get_user_model().objects.all()

    if request.method == 'POST':
        commentForm = ReviewForm(request.POST)
        if commentForm.is_valid():
            postReview = commentForm.save(commit=False)
            postReview.reviewModID = Mod.objects.get(modID=post.modID)
            #postReview.reviewAuthor = request.user
            postReview.reviewAuthorID = request.user
            postReview.save()
            user = User.objects.get(id=request.user.id)
            user.totalComments = user.totalComments + 1
            user.save()
            return redirect('mod:modPage', pk=post.pk)
    else:
        commentForm = ReviewForm()
    return render(request, 'mod/modPage.html', {'post': post, 'commentForm': commentForm, 'review': review,
                                                'vote': vote, 'questions': questions, 'rating': rating, 'news': news,
                                                'newsnotifications': newsnotifications, 'emails': emails})


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
        group = Group.objects.get(name="Well respected")
        if allVotes >= 10:
            group.user_set.add(reviewrating.reviewAuthorID)#User.objects.get(id=reviewrating.reviewAuthorID))#User.objects.get(username=reviewrating.reviewAuthor).id))
        else:
            group.user_set.remove(reviewrating.reviewAuthorID)#User.objects.get(id=reviewrating.reviewAuthorID))#User.objects.get(username=reviewrating.reviewAuthor).id))
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
        group = Group.objects.get(name="Well respected")
        if allVotes >= 10:
            group.user_set.add(reviewrating.reviewAuthorID)#User.objects.get(id=reviewrating.reviewAuthorID))#User.objects.get(username=reviewrating.reviewAuthor).id))
        else:
            group.user_set.remove(reviewrating.reviewAuthorID)#User.objects.get(id=reviewrating.reviewAuthorID))#User.objects.get(username=reviewrating.reviewAuthor).id))
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
        group = Group.objects.get(name="Well respected")
        if votesAgg >= 10:
            group.user_set.add(reviewrating.reviewAuthorID)#User.objects.get(id=reviewrating.reviewAuthorID))#User.objects.get(username=reviewrating.reviewAuthor).id))
        else:
            group.user_set.remove(reviewrating.reviewAuthorID)#User.objects.get(id=reviewrating.reviewAuthorID))#User.objects.get(username=reviewrating.reviewAuthor).id))
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
        user = User.objects.get(id=request.user.id)
        user.totalComments = user.totalComments - 1
        user.save()

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
        modID.modRating = format(averageRating, ".1f")
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
        form = SubmitForm(request.POST, request.FILES, instance=post)
        #form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            #post.modID = pk
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
    if request.user == post.modAuthor:
        post.delete()
        user = User.objects.get(id=request.user.id)
        user.totalMods = user.totalMods - 1
        user.save()
        group = Group.objects.get(name="Mod Creators")
        group.user_set.remove(request.user)
        return redirect('accounts:profile')
    else:
        return HttpResponseForbidden("You can't delete other users mods!")


def news(request, pk):
    if request.method == 'POST':
        #newsForm = NewsForm(request.POST)
        #if newsForm.is_valid():
        news_text = request.POST.get('news_text')
        news_mod_id = request.POST.get('news_mod_id')

        post = News(newsModID=Mod.objects.get(modID=news_mod_id), newsText=news_text)
        post.save()
        responseData = {}

        toEmailList = list()
        modTitle = Mod.objects.get(modID=news_mod_id).modName
        recipients = NewsNotifications.objects.filter(newsNotificationsModID=Mod.objects.get(modID=news_mod_id))\
            .values_list('newsNotificationsUserID', flat=True)
        for x in recipients:
            emails = get_user_model().objects.filter(id=x).values('email')
            toEmailList.append(emails.first()['email'])
        #for x in emails:
        #    yaes.append(x)

        if len(toEmailList) == 0:
            pass
        else:
            notificationsSendMail(modTitle, toEmailList, news_text)

        responseData['result'] = "Successfully added news to {0}.".format(news_mod_id)

        return HttpResponse(
            json.dumps(responseData),
            content_type='application/json'
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type='application/json'
        )


def notification(request, pk):
    if request.method == 'POST':
        modID = request.POST.get('modID')
        follow = request.POST.get('follow')
        responseData = {}

        if follow == 'add':  # adding to notifications
            post = NewsNotifications(newsNotificationsModID=Mod.objects.get(modID=modID), newsNotificationsUserID=request.user)
            post.save()

            responseData['result'] = "Successfully following mod {0}.".format(modID)

            return HttpResponse(
                json.dumps(responseData),
                content_type='application/json'
            )

        elif follow == 'remove':  # removing from notifications
            NewsNotifications.objects.get(newsNotificationsModID=Mod.objects.get(modID=modID),
                                          newsNotificationsUserID=request.user).delete()

            responseData['result'] = "Successfully removed the notification from mod {0}.".format(modID)

            return HttpResponse(
                json.dumps(responseData),
                content_type='application/json'
            )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type='application/json'
        )




def modTagFilter(request):
    mods = Mod.objects.filter(tags__name__in=["depressing", "sad"]).distinct()
    tags = Tag.objects.all()

    return render(request, 'mod/modTagFilter.html', {'mods': mods, 'tags': tags})


class SearchResultsView(ListView):
    model = Mod
    template_name = 'mod/modSearch.html'

    def get_queryset(self):
        searchQuery = self.request.GET.get('search')
        tagFilter = self.request.GET.getlist('tags')
        ay = len(tagFilter)
        if tagFilter is None and searchQuery is not None:
            object_list = Mod.objects.filter(
                Q(modName__contains=searchQuery) | Q(modDescription__contains=searchQuery)
            )
        elif searchQuery is None and tagFilter is not None:
            object_list = Mod.objects.filter(
                tags__name__in=tagFilter
            )
        elif searchQuery is not None and tagFilter is not None:
            object_list = Mod.objects.filter(
                Q(modName__contains=searchQuery) | Q(modDescription__contains=searchQuery)
            ).filter(tags__name__in=tagFilter)\
                .annotate(num_tags=Count('tags'))\
                .filter(num_tags=len(tagFilter))#.filter(tags__name__in=[tagFilter[0]]).filter(tags__name__in=[tagFilter[1]]).distinct()
            #for x in tagFilter:
            #    object_list.filter(tags__name__in=[x])
        else:
            return HttpResponse("Please enter something in the search parameter")
        return object_list

    def get_tags(self):
        tags = Tag.objects.all()
        return tags
