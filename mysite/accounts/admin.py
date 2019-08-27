from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import get_user_model

# Register your models here.

#admin.site.register(User, UserAdmin)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username', 'description']


admin.site.register(User, CustomUserAdmin)
