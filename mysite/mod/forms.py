from django import forms

class SubmitForm(forms.Form):
    modName = forms.CharField(label='Mod name', max_length=100)
    modDescription = forms.CharField(label='Mod description', max_length=10000)
    modWebsite = forms.CharField(label='Mod website', max_length=100)
    modTag = forms.CharField(label='Mod tags', max_length=1000)
    modCreditPerms = forms.CharField(label='Mod credits and permissions', max_length=1000)
    modDonations = forms.CharField(label='Mod donations', max_length=1000)
    modDiscord = forms.CharField(label='Mod Discord', max_length=100)
