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
from django.views.generic import TemplateView, FormView
from django.db.models import F, Q, Count, Sum, Avg
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core import serializers, mail
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import Http404

import json, pdb, math, datetime

from django_filters.views import FilterView
from taggit.models import Tag
from PIL import Image

from .forms import SubmitForm, ReviewForm, NewsForm, EditForm
from .models import Mod, ReviewRating, Rating, News, NewsNotifications, Vote, ModEdit, EditReviewRating  # , ModFilter
from .scripts import moveMod
from .operations.mail import notificationsSendMail
from .scripts import removeEdit

from accounts.models import User


# Create your views here.

def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    return render(request, 'mod/index.html')


@login_required
def submit(request):
    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.modAuthor = request.user
            #post.modDate = timezone.now()
            post.modUpdate = timezone.now()
            post.modShow = False
            post.modIP = visitor_ip_address(request)
            post.save()
            post.save()
            form.save_m2m()
            post.tags.add("All")
            for x in post.tags.names():
                print(x)
                if str(x) == "nsfw":
                    post.modNSFW = True
            post.modShow = False
            post.save()
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
    if not post.modIP:
        return render(request, 'mod/modPage.html', {'post': post})
    else:
        pass
    review = ReviewRating.objects.filter(reviewModID=post.modID)
    vote = Vote.objects.all()
    if request.user.is_authenticated:
        try:
            rating = Rating.objects.get(ratingAuthorID=request.user, ratingModID=post.modID)
        except ObjectDoesNotExist:
            rating = None
    else:
        rating = None

    questions = ReviewRating.objects.annotate(number_of_votes=Sum('reviewVotes'))

    post.tags = Tag.objects.all()

    news = News.objects.filter(newsModID=pk)

    if request.user.is_authenticated:
        try:
            newsnotifications = NewsNotifications.objects.get(newsNotificationsUserID=request.user.id, newsNotificationsModID=pk)
        except ObjectDoesNotExist:
            newsnotifications = None
    else:
        newsnotifications = None

    emails = get_user_model().objects.all()  # czech it

    if request.method == 'POST':
        commentForm = ReviewForm(request.POST)
        if commentForm.is_valid():
            postReview = commentForm.save(commit=False)
            postReview.reviewModID = Mod.objects.get(modID=post.modID)
            # postReview.reviewAuthor = request.user
            postReview.reviewAuthorID = request.user
            postReview.reviewApproved = False
            postReview.save()
            user = User.objects.get(id=request.user.id)
            user.totalComments = user.totalComments + 1
            user.save()
            return redirect('mod:modPage', pk=post.pk)
    else:
        commentForm = ReviewForm()
    return render(request, 'mod/modPage.html', {'post': post, 'commentForm': commentForm, 'review': review,
                                                'questions': questions, 'rating': rating, 'news': news,
                                                'newsnotifications': newsnotifications, 'emails': emails, 'vote': vote})


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
            group.user_set.add(
                reviewrating.reviewAuthorID)  # User.objects.get(id=reviewrating.reviewAuthorID))#User.objects.get(username=reviewrating.reviewAuthor).id))
        else:
            group.user_set.remove(
                reviewrating.reviewAuthorID)  # User.objects.get(id=reviewrating.reviewAuthorID))#User.objects.get(username=reviewrating.reviewAuthor).id))
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
            group.user_set.add(
                reviewrating.reviewAuthorID)  # User.objects.get(id=reviewrating.reviewAuthorID))#User.objects.get(username=reviewrating.reviewAuthor).id))
        else:
            group.user_set.remove(
                reviewrating.reviewAuthorID)  # User.objects.get(id=reviewrating.reviewAuthorID))#User.objects.get(username=reviewrating.reviewAuthor).id))
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
        votesAgg = Vote.objects.filter(voteReviewID__exact=request_getdata).aggregate(totalVoted=Sum('voteValue'))[
            'totalVoted']
        # allVotes = Vote.objects.aggregate(totalVoted=Sum(votesAgg))
        reviewrating.reviewVotes = votesAgg
        reviewrating.save()
        group = Group.objects.get(name="Well respected")
        if votesAgg >= 10:
            group.user_set.add(
                reviewrating.reviewAuthorID)  # User.objects.get(id=reviewrating.reviewAuthorID))#User.objects.get(username=reviewrating.reviewAuthor).id))
        else:
            group.user_set.remove(
                reviewrating.reviewAuthorID)  # User.objects.get(id=reviewrating.reviewAuthorID))#User.objects.get(username=reviewrating.reviewAuthor).id))
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
        try:
            EditReviewRating.objects.get(reviewid__exact=request_getdata).delete()
        except ObjectDoesNotExist:
            pass
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


@login_required
def reviewEdit(request, pk):
    if request.method == 'POST':
        reviewID = request.POST.get('id')
        reviewComment = request.POST.get('comment')
        review = ReviewRating.objects.get(reviewid__exact=reviewID)
        try:
            EditReviewRating.objects.get(reviewid__exact=reviewID).delete()
        except ObjectDoesNotExist:
            pass
        editReview = EditReviewRating(reviewid=reviewID, reviewDate=timezone.now(), reviewComment=reviewComment)
        review.reviewHasEdit = True
        review.save()
        editReview.save()

        response_data = {}
        response_data['result'] = "Successfully edited review " + reviewID

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
        request_radioValue = request.POST.get('radioValue')
        request_selectedChoice = request.POST.get('selectedChoice')

        modID = Mod.objects.get(modID__exact=request_modID)

        try:
            Rating.objects.get(ratingModID=modID, ratingAuthorID=request.user).delete()
        except ObjectDoesNotExist:
            pass

        response_data = {}
        if request_radioValue == "N/A":
            post = Rating(ratingModID=modID, ratingAuthorID=request.user, ratingChoice=request_selectedChoice)
        else:
            post = Rating(ratingModID=modID, ratingAuthorID=request.user, ratingChoice=request_selectedChoice,
                          ratingValue=request_radioValue)
        post.save()

        averageRating = Rating.objects.filter(ratingModID=request_modID).aggregate(Avg(('ratingValue')))[
            'ratingValue__avg']  # getting average rating for the mod we are using
        modID.modRating = format(averageRating, ".1f")
        modID.save()  # updating mod average rating

        response_data['result'] = "Successfully rated mod {0} with a {1}/5.".format(request_modID, request_radioValue)
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


def ratingDelete(request):
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


@login_required
def modEdit(request, pk):
    mod = get_object_or_404(Mod, pk=pk)  # dont need to pass entire object
    try:
        if (get_object_or_404(ModEdit, modID=pk)):
            alreadyEdited = True
    except Http404:
        alreadyEdited = False
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                oldEdit = get_object_or_404(ModEdit, modID=pk)
                removeEdit(oldEdit, mod)
                oldEdit.delete()
                alreadyEdited = True
            except:
                pass
            post = form.save(commit=False)
            if mod.modPreviewImage1 and post.modPreviewImage1 == "" and request.POST.get(
                    "modPreviewImage1-clear") != "on":
                post.modPreviewImage1 = mod.modPreviewImage1
            if mod.modPreviewImage2 and post.modPreviewImage2 == "" and request.POST.get(
                    "modPreviewImage2-clear") != "on":
                post.modPreviewImage2 = mod.modPreviewImage2
            if mod.modPreviewImage3 and post.modPreviewImage3 == "" and request.POST.get(
                    "modPreviewImage3-clear") != "on":
                post.modPreviewImage3 = mod.modPreviewImage3
            if mod.modPreviewImage4 and post.modPreviewImage4 == "" and request.POST.get(
                    "modPreviewImage4-clear") != "on":
                post.modPreviewImage4 = mod.modPreviewImage4
            if mod.modPreviewImage5 and post.modPreviewImage5 == "" and request.POST.get(
                    "modPreviewImage5-clear") != "on":
                post.modPreviewImage5 = mod.modPreviewImage5
            if mod.modBackground and post.modBackground == "" and request.POST.get("modBackground-clear") != "on":
                post.modBackground = mod.modBackground
            if mod.modAvatar and post.modAvatar == "" and request.POST.get("modAvatar-clear") != "on":
                post.modAvatar = mod.modAvatar
            post.modAuthor = request.user
            post.modDate = timezone.now()
            post.modUpdate = timezone.now()
            post.modID = pk
            post.modIP = visitor_ip_address(request)
            post.save()
            post.save()
            mod.modEdited = True
            for x in post.tags.names():
                if x == "nsfw":
                    print(x)
                    post.modNSFW = True
            post.save()
            mod.save()
            form.save_m2m()
            return redirect('mod:modPage', pk=mod.pk)
    else:
        form = EditForm(instance=mod)
        form.errors.as_data()
    print("No POST, probably loading page for first time")
    return render(request, 'mod/modEdit.html', {'form': form, 'post': mod, 'alreadyEdited': alreadyEdited},
                  content_type="text/html")


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
        # newsForm = NewsForm(request.POST)
        # if newsForm.is_valid():
        news_text = request.POST.get('news_text')
        news_mod_id = request.POST.get('news_mod_id')

        post = News(newsModID=Mod.objects.get(modID=news_mod_id), newsText=news_text,
                    newsIP=visitor_ip_address(request))
        post.save()
        responseData = {}

        toEmailList = list()
        modTitle = Mod.objects.get(modID=news_mod_id).modName
        recipients = NewsNotifications.objects.filter(newsNotificationsModID=Mod.objects.get(modID=news_mod_id)) \
            .values_list('newsNotificationsUserID', flat=True)
        for x in recipients:
            emails = get_user_model().objects.filter(id=x).values('email')
            toEmailList.append(emails.first()['email'])
        # for x in emails:
        #    yaes.append(x)

        if len(toEmailList) == 0:
            pass
        else:
            notificationsSendMail(modTitle, toEmailList, news_text, news_mod_id)

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
            post = NewsNotifications(newsNotificationsModID=Mod.objects.get(modID=modID),
                                     newsNotificationsUserID=request.user)
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
        searchQuery = self.request.GET.get('q').title()  # also added title
        tagFilter = self.request.GET.getlist('tags')
        sortBy = self.request.GET.get('sortBy')
        dateBy = self.request.GET.get('dateBy')
        dateBy = int(dateBy)

        datetime.datetime.now(tz=timezone.utc)
        today = datetime.date.today()
        today = timezone.now()

        if int(dateBy) == 0:
            dateBy = 99999  # I am ashamed of this code, but it's the easiest solution
            # STOP JUDGING ME, MY BRAIN IS BAD

        if (searchQuery is "" or None) and (len(tagFilter) == 0):
            print(1)
            if sortBy == 'newest':
                object_list = Mod.objects.all().order_by('-modDate').filter(
                    modDate__gte=today - datetime.timedelta(days=dateBy)).filter(modShow=True)
            if sortBy == 'rated':
                object_list = Mod.objects.all().order_by('-modRating').filter(
                    modDate__gte=today - datetime.timedelta(days=dateBy)).filter(modShow=True)
            if sortBy == 'reviewed':
                object_list = sorted(Mod.objects.all().filter(modDate__gte=today - datetime.timedelta(days=dateBy)).filter(modShow=True),
                                     key=lambda x: x.modReviewCount, reverse=True)
            if sortBy == 'oldest':
                object_list = Mod.objects.all().order_by('modDate').filter(
                    modDate__gte=today - datetime.timedelta(days=dateBy)).filter(modShow=True)
            if sortBy == 'updated':
                object_list = Mod.objects.all().order_by('-modUpdate').filter(
                    modDate__gte=today - datetime.timedelta(days=dateBy)).filter(modShow=True)

        elif (tagFilter is "" or len(tagFilter) == 0) and (searchQuery is not "" or None):
            print(2)
            if sortBy == 'newest':
                object_list = Mod.objects.filter(
                    Q(modName__contains=searchQuery) | Q(modDescription__contains=searchQuery)
                ).order_by('-modDate').filter(modDate__gte=today - datetime.timedelta(days=dateBy)).filter(
                    modShow=True).order_by(
                    '-modDate')  # i removed the .filter.annotate fix present in others, incase it all goes wrong
            elif sortBy == 'rated':
                object_list = Mod.objects.filter(
                    Q(modName__contains=searchQuery) | Q(modDescription__contains=searchQuery)
                ).order_by('-modRating').filter(modDate__gte=today - datetime.timedelta(days=dateBy)).filter(
                    modShow=True).order_by('-modDate')
            elif sortBy == 'reviewed':
                object_list = sorted(Mod.objects.filter(
                    Q(modName__contains=searchQuery) | Q(modDescription__contains=searchQuery)
                ).filter(modDate__gte=today - datetime.timedelta(days=dateBy)).filter(modShow=True).order_by(
                    '-modDate'), key=lambda x: x.modReviewCount, reverse=True)
            elif sortBy == 'oldest':
                object_list = Mod.objects.filter(
                    Q(modName__contains=searchQuery) | Q(modDescription__contains=searchQuery)
                ).order_by('modDate').filter(modDate__gte=today - datetime.timedelta(days=dateBy)).filter(
                    modShow=True).order_by('-modDate')
            elif sortBy == 'updated':
                object_list = Mod.objects.filter(
                    Q(modName__contains=searchQuery) | Q(modDescription__contains=searchQuery)
                ).order_by('-modUpdate').filter(modDate__gte=today - datetime.timedelta(days=dateBy)).filter(
                    modShow=True).order_by('-modDate')
            else:
                object_list = Mod.objects.filter(
                    Q(modName__contains=searchQuery) | Q(modDescription__contains=searchQuery)
                ).filter(modDate__gte=today - datetime.timedelta(days=dateBy)).filter(modShow=True).order_by('-modDate')

        elif (searchQuery is "" or None) and (tagFilter is not "" or len(tagFilter) == 0):
            print(3)
            if sortBy == 'newest':
                object_list = Mod.objects.all().filter(tags__name__in=tagFilter).annotate(
                    num_tags=Count('tags')).filter(num_tags=len(tagFilter)).filter(modShow=True).order_by(
                    '-modDate').filter(modDate__gte=today - datetime.timedelta(days=int(dateBy)))
                # object_list = Mod.objects.filter(
                #    tags__name__in=tagFilter
                # ).filter(tags__name__in=tagFilter).annotate(num_tags=Count('tags')).filter(num_tags=len(tagFilter)).order_by('-modDate').filter(modDate__gte=today - datetime.timedelta(days=int(dateBy)))
            elif sortBy == 'rated':
                object_list = Mod.objects.all().filter(tags__name__in=tagFilter).annotate(
                    num_tags=Count('tags')).filter(num_tags=len(tagFilter)).filter(modShow=True).order_by(
                    '-modRating').filter(modDate__gte=today - datetime.timedelta(days=int(dateBy)))
                # object_list = Mod.objects.filter(
                #    tags__name__in=tagFilter
                # ).filter(tags__name__in=tagFilter).annotate(num_tags=Count('tags')).filter(num_tags=len(tagFilter)).order_by('-modRating').filter(modDate__gte=today - datetime.timedelta(days=int(dateBy)))
            elif sortBy == 'reviewed':
                object_list = sorted(
                    Mod.objects.all().filter(tags__name__in=tagFilter).annotate(num_tags=Count('tags')).filter(
                        num_tags=len(tagFilter)).filter(modShow=True).filter(
                        modDate__gte=today - datetime.timedelta(days=int(dateBy))), key=lambda x: x.modReviewCount,
                    reverse=True)
                # object_list = sorted(Mod.objects.filter(
                #    tags__name__in=tagFilter
                # ).filter(tags__name__in=tagFilter).annotate(num_tags=Count('tags')).filter(num_tags=len(tagFilter)).filter(modDate__gte=today - datetime.timedelta(days=int(dateBy))), key=lambda x: x.modReviewCount, reverse=True)
            elif sortBy == 'oldest':
                object_list = Mod.objects.all().filter(tags__name__in=tagFilter).annotate(
                    num_tags=Count('tags')).filter(num_tags=len(tagFilter)).filter(modShow=True).order_by(
                    'modDate').filter(modDate__gte=today - datetime.timedelta(days=int(dateBy)))
                # object_list = Mod.objects.filter(
                #    tags__name__in=tagFilter
                # ).filter(tags__name__in=tagFilter).annotate(num_tags=Count('tags')).filter(num_tags=len(tagFilter)).order_by('modDate').filter(modDate__gte=today - datetime.timedelta(days=int(dateBy)))
            elif sortBy == 'updated':
                object_list = Mod.objects.all().filter(tags__name__in=tagFilter).annotate(
                    num_tags=Count('tags')).filter(num_tags=len(tagFilter)).filter(modShow=True).order_by(
                    '-modUpdate').filter(modDate__gte=today - datetime.timedelta(days=int(dateBy)))
                # object_list = Mod.objects.filter(
                #    tags__name__in=tagFilter
                # ).filter(tags__name__in=tagFilter).annotate(num_tags=Count('tags')).filter(num_tags=len(tagFilter)).order_by('-modUpdate').filter(modDate__gte=today - datetime.timedelta(days=int(dateBy)))
            else:
                object_list = Mod.objects.all().filter(tags__name__in=tagFilter).annotate(
                    num_tags=Count('tags')).filter(num_tags=len(tagFilter)).filter(modShow=True).filter(
                    modDate__gte=today - datetime.timedelta(days=int(dateBy)))
                # object_list = Mod.objects.filter(
                #    tags__name__in=tagFilter
                # ).filter(tags__name__in=tagFilter).annotate(num_tags=Count('tags')).filter(num_tags=len(tagFilter)).filter(modDate__gte=today - datetime.timedelta(days=int(dateBy)))

        elif (searchQuery is not "" or None) and (tagFilter is not "" or len(tagFilter) == 0):
            print(4)
            if sortBy == 'newest':
                object_list = Mod.objects.filter(
                    Q(modName__contains=searchQuery) | Q(modDescription__contains=searchQuery)
                ).filter(tags__name__in=tagFilter).annotate(num_tags=Count('tags')).filter(
                    num_tags=len(tagFilter)).filter(modShow=True).order_by('-modDate').filter(
                    modDate__gte=today - datetime.timedelta(days=dateBy))
            elif sortBy == 'rated':
                object_list = Mod.objects.filter(
                    Q(modName__contains=searchQuery) | Q(modDescription__contains=searchQuery)
                ).filter(tags__name__in=tagFilter).annotate(num_tags=Count('tags')).filter(
                    num_tags=len(tagFilter)).filter(modShow=True).order_by('-modRating').filter(
                    modDate__gte=today - datetime.timedelta(days=dateBy))
            elif sortBy == 'reviewed':
                object_list = sorted(Mod.objects.filter(
                    Q(modName__contains=searchQuery) | Q(modDescription__contains=searchQuery)
                ).filter(tags__name__in=tagFilter).annotate(num_tags=Count('tags')).filter(
                    num_tags=len(tagFilter)).filter(modShow=True).filter(
                    modDate__gte=today - datetime.timedelta(days=dateBy)), key=lambda x: x.modReviewCount, reverse=True)
            elif sortBy == 'oldest':
                object_list = Mod.objects.filter(
                    Q(modName__contains=searchQuery) | Q(modDescription__contains=searchQuery)
                ).filter(tags__name__in=tagFilter).annotate(num_tags=Count('tags')).filter(
                    num_tags=len(tagFilter)).filter(modShow=True).order_by('modDate').filter(
                    modDate__gte=today - datetime.timedelta(days=dateBy))
            elif sortBy == 'updated':
                object_list = Mod.objects.filter(
                    Q(modName__contains=searchQuery) | Q(modDescription__contains=searchQuery)
                ).filter(tags__name__in=tagFilter).annotate(num_tags=Count('tags')).filter(
                    num_tags=len(tagFilter)).filter(modShow=True).order_by('-modUpdate').filter(
                    modDate__gte=today - datetime.timedelta(days=dateBy))
            else:
                object_list = Mod.objects.filter(
                    Q(modName__contains=searchQuery) | Q(modDescription__contains=searchQuery)
                ).filter(tags__name__in=tagFilter).annotate(num_tags=Count('tags')).filter(
                    num_tags=len(tagFilter)).filter(modShow=True).filter(
                    modDate__gte=today - datetime.timedelta(days=dateBy))

        else:
            return HttpResponse("Please enter something in the search parameter")
        return object_list

    def get_tags(self):
        tags = Tag.objects.all()
        return tags


def latest(request):
    post = Mod.objects.filter(modShow=True).order_by("-modDate")[0]
    return render(request, 'mod/modLatest.html', {'post': post})

def awards2018(request):
    if settings.DEBUG == False:
        MotYFirstPlace = Mod.objects.get(modID=55)
        #MotYRunnerUp = Mod.objects.get(modID=69)
        SayoriFirstPlace = Mod.objects.get(modID=55)
        SayoriRunnerUp = Mod.objects.get(modID=4)
        YuriFirstPlace = Mod.objects.get(modID=87)
        YuriRunnerUp = Mod.objects.get(modID=59)
        MonikaFirstPlace = Mod.objects.get(modID=7)
        MonikaRunnerUp = Mod.objects.get(modID=8)
        #NatsukiFirstPlace = Mod.objects.get(modID=11)
        #NatsukiRunnerUp = Mod.objects.get(modID=12)
        #AllRounderFirstPlace = Mod.objects.get(modID=13)
        AllRounderRunnerUp = Mod.objects.get(modID=86)
        #EmotionalFirstPlace = Mod.objects.get(modID=15)
        EmotionalRunnerUp = Mod.objects.get(modID=4)
        LightheartedFirstPlace = Mod.objects.get(modID=1)
        #LightheartedRunnerUp = Mod.objects.get(modID=34)
        #InnovativeFirstPlace = Mod.objects.get(modID=21)
        InnovativeRunnerUp = Mod.objects.get(modID=55)
    else:
        MotYFirstPlace = Mod.objects.get(modID=22)
        MotYRunnerUp = Mod.objects.get(modID=22)
        SayoriFirstPlace = Mod.objects.get(modID=22)
        SayoriRunnerUp = Mod.objects.get(modID=22)
        YuriFirstPlace = Mod.objects.get(modID=22)
        YuriRunnerUp = Mod.objects.get(modID=22)
        MonikaFirstPlace = Mod.objects.get(modID=22)
        MonikaRunnerUp = Mod.objects.get(modID=8)
        #NatsukiFirstPlace = Mod.objects.get(modID=11)
        #NatsukiRunnerUp = Mod.objects.get(modID=12)
        #AllRounderFirstPlace = Mod.objects.get(modID=13)
        AllRounderRunnerUp = Mod.objects.get(modID=14)
        EmotionalFirstPlace = Mod.objects.get(modID=15)
        EmotionalRunnerUp = Mod.objects.get(modID=25)
        LightheartedFirstPlace = Mod.objects.get(modID=17)
        #LightheartedRunnerUp = Mod.objects.get(modID=19)
        InnovativeFirstPlace = Mod.objects.get(modID=21)
        InnovativeRunnerUp = Mod.objects.get(modID=22)
    return render(request, 'mod/awards2018.html', {'MotYFirstPlace': MotYFirstPlace,
                                                   #'MotYRunnerUp': MotYRunnerUp,
                                                   'SayoriFirstPlace': SayoriFirstPlace,
                                                   'SayoriRunnerUp': SayoriRunnerUp,
                                                   'YuriFirstPlace': YuriFirstPlace,
                                                   'YuriRunnerUp': YuriRunnerUp,
                                                   'MonikaFirstPlace': MonikaFirstPlace,
                                                   'MonikaRunnerUp': MonikaRunnerUp,
                                                   #'NatsukiFirstPlace': NatsukiFirstPlace,
                                                   #'NatsukiRunnerUp': NatsukiRunnerUp,
                                                   #'AllRounderFirstPlace': AllRounderFirstPlace,
                                                   'AllRounderRunnerUp': AllRounderRunnerUp,
                                                   #'EmotionalFirstPlace': EmotionalFirstPlace,
                                                   'EmotionalRunnerUp': EmotionalRunnerUp,
                                                   'LightheartedFirstPlace': LightheartedFirstPlace,
                                                   #'LightheartedRunnerUp': LightheartedRunnerUp,
                                                   #'InnovativeFirstPlace': InnovativeFirstPlace,
                                                   'InnovativeRunnerUp': InnovativeRunnerUp})


def awards2019(request):
    if settings.DEBUG == False:
        MotYFirstPlace = Mod.objects.get(modID=89)
        MotYRunnerUp = Mod.objects.get(modID=63)
        SayoriFirstPlace = Mod.objects.get(modID=15)
        SayoriRunnerUp = Mod.objects.get(modID=61)
        YuriFirstPlace = Mod.objects.get(modID=92)
        YuriRunnerUp = Mod.objects.get(modID=79)
        #MonikaFirstPlace = Mod.objects.get(modID=22)
        MonikaRunnerUp = Mod.objects.get(modID=75)
        NatsukiFirstPlace = Mod.objects.get(modID=63)
        NatsukiRunnerUp = Mod.objects.get(modID=87)
        AllRounderFirstPlace = Mod.objects.get(modID=86)
        AllRounderRunnerUp = Mod.objects.get(modID=15)
        EmotionalFirstPlace = Mod.objects.get(modID=92)
        EmotionalRunnerUp = Mod.objects.get(modID=87)
        LightheartedFirstPlace = Mod.objects.get(modID=89)
        LightheartedRunnerUp = Mod.objects.get(modID=61)
        InnovativeFirstPlace = Mod.objects.get(modID=63)
        InnovativeRunnerUp = Mod.objects.get(modID=61)
        OriginalArtworkFirstPlace = Mod.objects.get(modID=86)
        OriginalArtworkRunnerUp = Mod.objects.get(modID=149)
    else:
        MotYFirstPlace = Mod.objects.get(modID=22)
        MotYRunnerUp = Mod.objects.get(modID=22)
        SayoriFirstPlace = Mod.objects.get(modID=22)
        SayoriRunnerUp = Mod.objects.get(modID=22)
        YuriFirstPlace = Mod.objects.get(modID=22)
        YuriRunnerUp = Mod.objects.get(modID=22)
        #MonikaFirstPlace = Mod.objects.get(modID=22)
        MonikaRunnerUp = Mod.objects.get(modID=22)
        NatsukiFirstPlace = Mod.objects.get(modID=22)
        NatsukiRunnerUp = Mod.objects.get(modID=22)
        AllRounderFirstPlace = Mod.objects.get(modID=22)
        AllRounderRunnerUp = Mod.objects.get(modID=22)
        EmotionalFirstPlace = Mod.objects.get(modID=22)
        EmotionalRunnerUp = Mod.objects.get(modID=22)
        LightheartedFirstPlace = Mod.objects.get(modID=22)
        LightheartedRunnerUp = Mod.objects.get(modID=22)
        InnovativeFirstPlace = Mod.objects.get(modID=22)
        InnovativeRunnerUp = Mod.objects.get(modID=22)
        OriginalArtworkFirstPlace = Mod.objects.get(modID=22)
        OriginalArtworkRunnerUp = Mod.objects.get(modID=22)
    return render(request, 'mod/awards2019.html', {'MotYFirstPlace': MotYFirstPlace,
                                                   'MotYRunnerUp': MotYRunnerUp,
                                                   'SayoriFirstPlace': SayoriFirstPlace,
                                                   'SayoriRunnerUp': SayoriRunnerUp,
                                                   'YuriFirstPlace': YuriFirstPlace,
                                                   'YuriRunnerUp': YuriRunnerUp,
                                                   #'MonikaFirstPlace': MonikaFirstPlace,
                                                   'MonikaRunnerUp': MonikaRunnerUp,
                                                   'NatsukiFirstPlace': NatsukiFirstPlace,
                                                   'NatsukiRunnerUp': NatsukiRunnerUp,
                                                   'AllRounderFirstPlace': AllRounderFirstPlace,
                                                   'AllRounderRunnerUp': AllRounderRunnerUp,
                                                   'EmotionalFirstPlace': EmotionalFirstPlace,
                                                   'EmotionalRunnerUp': EmotionalRunnerUp,
                                                   'LightheartedFirstPlace': LightheartedFirstPlace,
                                                   'LightheartedRunnerUp': LightheartedRunnerUp,
                                                   'InnovativeFirstPlace': InnovativeFirstPlace,
                                                   'InnovativeRunnerUp': InnovativeRunnerUp,
                                                   'OriginalArtworkFirstPlace': OriginalArtworkFirstPlace,
                                                   'OriginalArtworkRunnerUp': OriginalArtworkRunnerUp})