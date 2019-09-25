from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Avatar
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import get_user_model

# Register your models here.

#admin.site.register(User, UserAdmin)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('description', 'totalComments', 'totalMods')}),
    )
    list_display = ['email', 'username', 'description', 'totalComments', 'totalMods']


class AvatarAdmin(admin.ModelAdmin):
    list_display = ['avatarID', 'avatarUserID', 'avatarTime', 'avatarImage', 'avatarApproved']


admin.site.register(User, CustomUserAdmin)
admin.site.register(Avatar, AvatarAdmin)
