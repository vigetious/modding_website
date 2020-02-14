from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.shortcuts import get_object_or_404

from .models import Mod, ReviewRating, Rating, News, NewsNotifications, Vote, ModEdit, EditReviewRating
from .scripts import removeEdit

import time

# Register your models here.


def mark_as_unsafe(modeladmin, request, queryset):
    queryset.update(modApproved=False)


mark_as_unsafe.short_description = "Mark has non-approved"


class ModAdmin(admin.ModelAdmin):
    list_display = ['modID', 'modEdited', 'modShow', 'modAuthor', 'modDate', 'modUpdate', 'modStatus', 'modName',
                    'modDescription', 'tags', 'modUpload', 'modUploadURL', 'modPlayTimeHours',
                    'modPlayTimeMinutes', 'modReviewCount', 'modIP']
    formfield_overrides = {
        models.CharField: {'widget': Textarea()}
    }
    ordering = ('modShow',)

    #change_form_template = 'progressbarupload/change_form.html'
    #add_form_template = 'progressbarupload/change_form.html'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

class ModEditAdmin(admin.ModelAdmin):
    list_display = ['modEditID', 'modID', 'modAuthor', 'modDate', 'modUpdate', 'modStatus', 'modName',
                    'modDescription', 'tags', 'modUpload', 'modUploadURL', 'modPlayTimeHours',
                    'modPlayTimeMinutes', 'modReviewCount', 'modIP']
    #actions = [mark_as_safe, mark_as_unsafe]
    formfield_overrides = {
        models.CharField: {'widget': Textarea()}
    }

    def get_actions(self, request):
        #Disable delete
        actions = super(ModEditAdmin, self).get_actions(request)
        #del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False

    def approve_edit(self, request, queryset):
        for x in queryset:
            originalMod = get_object_or_404(Mod, pk=x.modID)
            originalMod.modAuthor = x.modAuthor
            originalMod.modDate = x.modDate
            originalMod.modUpdate = x.modUpdate
            originalMod.modStatus = x.modStatus
            originalMod.modName = x.modName
            originalMod.modDescription = x.modDescription
            originalMod.modShortDescription = x.modShortDescription
            originalMod.modWebsite = x.modWebsite
            originalMod.tags = x.tags
            originalMod.modUpload = x.modUpload
            originalMod.modUploadURL = x.modUploadURL
            originalMod.modPlayTimeHours = x.modPlayTimeHours
            originalMod.modPlayTimeMinutes = x.modPlayTimeMinutes
            originalMod.modSearch = x.modSearch
            originalMod.modRating = x.modRating
            originalMod.modPreviewVideo = x.modPreviewVideo
            originalMod.modPreviewImage1 = x.modPreviewImage1
            originalMod.modPreviewImage2 = x.modPreviewImage2
            originalMod.modPreviewImage3 = x.modPreviewImage3
            originalMod.modPreviewImage4 = x.modPreviewImage4
            originalMod.modPreviewImage5 = x.modPreviewImage5
            originalMod.modBackground = x.modBackground
            originalMod.modBackgroundTiledStretch = x.modBackgroundTiledStretch
            originalMod.modAvatar = x.modAvatar
            originalMod.modIP = x.modIP
            originalMod.modNSFW = x.modNSFW
            originalMod.modEdited = False
            originalMod.save()
        self.message_user(request, "Edit successfully approved. Edits have gone live.")

        queryset.delete()

    def unapprove_edit(self, request, queryset):
        for x in queryset:
            removeEdit(x, get_object_or_404(Mod, pk=x.modID))
        queryset.delete()
        self.message_user(request, "Edit successfully removed. User can now make edits again.")


    actions = [approve_edit, unapprove_edit]

    #change_form_template = 'progressbarupload/change_form.html'
    #add_form_template = 'progressbarupload/change_form.html'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['reviewid', 'reviewModID', 'reviewAuthorID', 'reviewDate', 'reviewComment', 'vote_total',
                    'reviewVotes', 'reviewApproved']
    formfield_overrides = {
        models.CharField: {'widget': Textarea}
    }
    ordering = ('reviewApproved',)

    def mark_as_safe(modeladmin, request, queryset):
        queryset.update(reviewApproved=True)

    mark_as_safe.short_description = "Mark as approved"


    def mark_as_unsafe(modeladmin, request, queryset):
        queryset.update(reviewApproved=False)

    mark_as_unsafe.short_description = "Mark as non-approved"

    actions = [mark_as_safe, mark_as_unsafe]


class EditReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['reviewEditId', 'reviewid', 'reviewDate', 'reviewComment']
    formfield_overrides = {
        models.CharField: {'widget': Textarea}
    }
    ordering = ('reviewApproved',)

    def get_actions(self, request):
        #Disable delete
        actions = super(EditReviewRatingAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def approve_edit(self, request, queryset):
        for x in queryset:
            originalReview = ReviewRating.objects.get(reviewid__exact=x.reviewid)
            originalReview.reviewDate = x.reviewDate
            originalReview.reviewComment = x.reviewComment
            originalReview.reviewApproved = True
            originalReview.reviewHasEdit = False
            originalReview.save()
        queryset.delete()
        self.message_user(request, "Edit successfully approved. Edits have gone live.")

    def unapprove_edit(self, request, queryset):
        for x in queryset:
            originalReview = ReviewRating.objects.get(reviewid__exact=x.reviewid)
            originalReview.reviewApproved = True
            originalReview.reviewHasEdit = False
            originalReview.save()
        queryset.delete()
        self.message_user(request, "Edit successfully removed. User can now make edits again.")

    actions = [approve_edit, unapprove_edit]


class VoteAdmin(admin.ModelAdmin):
    list_display = ['voteID', 'voteReviewID', 'voteAuthor', 'voteValue']


class RatingAdmin(admin.ModelAdmin):
    list_display = ['ratingID', 'ratingModID', 'ratingAuthorID', 'ratingChoice', 'ratingValue']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['newsID', 'newsModID', 'newsDate', 'newsText']


class NewsNotificationsAdmin(admin.ModelAdmin):
    list_display = ['newsNotificationsID', 'newsNotificationsModID', 'newsNotificationsUserID']


admin.site.register(Mod, ModAdmin)
admin.site.register(ModEdit, ModEditAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(EditReviewRating, EditReviewRatingAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(NewsNotifications, NewsNotificationsAdmin)
