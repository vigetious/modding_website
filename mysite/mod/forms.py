from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from.models import Mod

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
        fields = ('modID', 'modName', 'modStatus', 'modDescription', 'modWebsite', 'modTag', 'modCreditPerms', 'modDonations', 'modDiscord', 'modUpload',)
