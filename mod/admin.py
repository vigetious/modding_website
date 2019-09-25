from django.contrib import admin

from .models import Mod, ReviewRating, Rating, News, NewsNotifications

# Register your models here.

class ModAdmin(admin.ModelAdmin):
    list_display = ['modID', 'modAuthor', 'modDate', 'modUpdate', 'modStatus', 'modName',
                    'modDescription', 'tags', 'modUpload', 'modUploadURL', 'modPlayTimeHours',
                    'modPlayTimeMinutes', 'modReviewCount', 'modApproved', 'modIP']

    #change_form_template = 'progressbarupload/change_form.html'
    #add_form_template = 'progressbarupload/change_form.html'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['reviewid', 'reviewModID', 'reviewAuthorID', 'reviewDate', 'reviewComment', 'vote_total',
                    'reviewVotes', 'reviewApproved']



class RatingAdmin(admin.ModelAdmin):
    list_display = ['ratingID', 'ratingModID', 'ratingAuthorID', 'ratingChoice', 'ratingValue']

class NewsAdmin(admin.ModelAdmin):
    list_display = ['newsID', 'newsModID', 'newsDate', 'newsText']

class NewsNotificationsAdmin(admin.ModelAdmin):
    list_display = ['newsNotificationsID', 'newsNotificationsModID', 'newsNotificationsUserID']


admin.site.register(Mod, ModAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)

admin.site.register(Rating, RatingAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(NewsNotifications, NewsNotificationsAdmin)
