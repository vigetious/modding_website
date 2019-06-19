from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def user(request):
    return render(request, 'user/accountPage.html')
