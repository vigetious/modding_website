from django.contrib import admin

from .models import Mod, ReviewRating, Vote, Rating

# Register your models here.

class ModAdmin(admin.ModelAdmin):
    list_display = ['modID', 'modAuthor', 'modDate', 'modUpdate', 'modDownloads', 'modStatus', 'modName',
                    'modDescription', 'modWebsite', 'tags', 'modCreditPerms', 'modDonations', 'modDiscord',
                    'modUpload', 'modUploadURL', 'modPlayTimeHours', 'modPlayTimeMinutes']#, 'modRating']

    change_form_template = 'progressbarupload/change_form.html'
    add_form_template = 'progressbarupload/change_form.html'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['reviewid', 'reviewModID', 'reviewAuthor', 'reviewDate', 'reviewComment', 'vote_total',
                    'reviewVotes']

class VoteAdmin(admin.ModelAdmin):
    list_display = ['voteID', 'voteReviewID', 'voteAuthor', 'voteValue']

class RatingAdmin(admin.ModelAdmin):
    list_display = ['ratingID', 'ratingModID', 'ratingAuthorID', 'ratingValue']


admin.site.register(Mod, ModAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Rating, RatingAdmin)
