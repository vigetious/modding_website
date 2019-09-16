from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from.models import Mod, ReviewRating, Vote, Rating, News

#class SubmitForm(forms.Form):
#    modName = forms.CharField(label='Mod name', max_length=100)
#    modDescription = forms.CharField(label='Mod description', max_length=10000)
#    modWebsite = forms.CharField(label='Mod website', max_length=100, validators=[URLValidator])
#    modTag = forms.CharField(label='Mod tags', max_length=1000)
#    modCreditPerms = forms.CharField(label='Mod credits and permissions', max_length=1000)
#    modDonations = forms.CharField(label='Mod donations', max_length=1000)
#    modSocial = forms.CharField(label='Mod Social', max_length=100)

#    def clean_modTag(self):
#        data = self.cleaned_data['modTag']
#        if '.' in data:
#            raise ValidationError(_('Invalid tags - tags cannot have full stops.'))
#        return data


class SubmitForm(forms.ModelForm):
    class Meta:
        model = Mod
        fields = ('modID', 'modName', 'modStatus', 'modDescription', 'modWebsite', 'tags', 'modCreditPerms',
                  'modDonations', 'modDiscord', 'modUpload', 'modUploadURL', 'modPlayTimeHours', 'modPlayTimeMinutes',
                  'modPreviewVideo', 'modPreviewImage1', 'modPreviewImage2', 'modPreviewImage3', 'modPreviewImage4',
                  'modPreviewImage5', 'modBackground', 'modBackgroundTiledStretch', 'modAvatar')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ('reviewid', 'reviewComment')


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('voteID', 'voteReviewID', 'voteAuthor', 'voteValue')


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('ratingID', 'ratingModID', 'ratingAuthorID', 'ratingValue')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('newsID', 'newsModID', 'newsText')
